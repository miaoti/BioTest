/**
 * BioTest Canonical JSON Harness for SAM parsing (C++ implementation).
 *
 * Usage: biotest_harness SAM <file_path>
 *
 * Reads a SAM file, outputs canonical JSON to stdout.
 * This harness is compiled alongside the SeqAn3 SUT to enable
 * coverage instrumentation of SeqAn3's parsing code paths.
 *
 * NOTE: For the initial version, we parse SAM text directly to produce
 * canonical JSON. Future versions will route through SeqAn3's
 * sam_file_input for coverage-instrumented execution.
 */

#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

// JSON string escaping
std::string json_str(std::string const & s) {
    std::string out = "\"";
    for (char c : s) {
        if (c == '"') out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else if (c == '\n') out += "\\n";
        else if (c == '\r') out += "\\r";
        else if (c == '\t') out += "\\t";
        else out += c;
    }
    out += "\"";
    return out;
}

// Parse a header tag line (@HD, @SQ, @RG, @PG) into JSON object
std::string parse_header_tags(std::istringstream & iss) {
    std::string tag, json = "{";
    bool first = true;
    while (iss >> tag) {
        auto pos = tag.find(':');
        if (pos != std::string::npos) {
            if (!first) json += ",";
            json += json_str(tag.substr(0, pos)) + ":"
                  + json_str(tag.substr(pos + 1));
            first = false;
        }
    }
    json += "}";
    return json;
}

int main(int argc, char * argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: biotest_harness SAM <file_path>\n";
        return 1;
    }

    std::string format = argv[1];
    std::string filepath = argv[2];

    if (format != "SAM") {
        std::cerr << "This harness only supports SAM format\n";
        return 1;
    }

    try {
        std::ifstream file(filepath);
        if (!file.is_open()) {
            std::cerr << "Cannot open file: " << filepath << "\n";
            return 1;
        }

        // --- Parse header ---
        std::string hd_json = "null";
        std::vector<std::string> sq_entries, rg_entries, pg_entries;
        std::vector<std::string> co_entries;
        std::vector<std::string> record_jsons;

        std::string line;
        while (std::getline(file, line)) {
            // Strip trailing \r
            if (!line.empty() && line.back() == '\r')
                line.pop_back();
            if (line.empty()) continue;

            if (line[0] == '@') {
                std::istringstream iss(line);
                std::string record_type;
                iss >> record_type;

                if (record_type == "@HD") {
                    hd_json = parse_header_tags(iss);
                } else if (record_type == "@SQ") {
                    sq_entries.push_back(parse_header_tags(iss));
                } else if (record_type == "@RG") {
                    rg_entries.push_back(parse_header_tags(iss));
                } else if (record_type == "@PG") {
                    pg_entries.push_back(parse_header_tags(iss));
                } else if (record_type == "@CO") {
                    auto co_pos = line.find('\t');
                    if (co_pos != std::string::npos)
                        co_entries.push_back(line.substr(co_pos + 1));
                }
                continue;
            }

            // --- Parse alignment record ---
            std::vector<std::string> cols;
            std::istringstream ss(line);
            std::string col;
            while (std::getline(ss, col, '\t'))
                cols.push_back(col);

            if (cols.size() < 11) continue;

            int flag = std::stoi(cols[1]);
            int pos_raw = std::stoi(cols[3]);
            int mapq = std::stoi(cols[4]);
            int pnext_raw = std::stoi(cols[7]);
            int tlen = std::stoi(cols[8]);

            std::ostringstream rj;
            rj << "{";
            rj << "\"QNAME\":" << json_str(cols[0]);
            rj << ",\"FLAG\":" << flag;
            rj << ",\"RNAME\":" << (cols[2] == "*" ? "null" : json_str(cols[2]));
            rj << ",\"POS\":" << (pos_raw == 0 ? "null" : std::to_string(pos_raw));
            rj << ",\"MAPQ\":" << mapq;

            // CIGAR
            if (cols[5] == "*") {
                rj << ",\"CIGAR\":null";
            } else {
                rj << ",\"CIGAR\":[";
                bool first_op = true;
                size_t i = 0;
                while (i < cols[5].size()) {
                    size_t j = i;
                    while (j < cols[5].size() && std::isdigit(cols[5][j])) ++j;
                    if (j < cols[5].size() && j > i) {
                        int len = std::stoi(cols[5].substr(i, j - i));
                        char op = cols[5][j];
                        if (!first_op) rj << ",";
                        rj << "{\"op\":\"" << op << "\",\"len\":" << len << "}";
                        first_op = false;
                    }
                    i = j + 1;
                }
                rj << "]";
            }

            rj << ",\"RNEXT\":" << (cols[6] == "*" ? "null" : json_str(cols[6]));
            rj << ",\"PNEXT\":" << (pnext_raw == 0 ? "null" : std::to_string(pnext_raw));
            rj << ",\"TLEN\":" << tlen;
            rj << ",\"SEQ\":" << (cols[9] == "*" ? "null" : json_str(cols[9]));
            rj << ",\"QUAL\":" << (cols[10] == "*" ? "null" : json_str(cols[10]));

            // Optional tags (cols 12+), sorted by key
            std::map<std::string, std::string> tags;
            for (size_t k = 11; k < cols.size(); ++k) {
                auto & t = cols[k];
                if (t.size() >= 5 && t[2] == ':' && t[4] == ':') {
                    std::string tag_name = t.substr(0, 2);
                    std::string tag_type(1, t[3]);
                    std::string tag_val = t.substr(5);

                    std::string val_json;
                    if (tag_type == "i") {
                        val_json = tag_val;
                    } else if (tag_type == "f") {
                        val_json = tag_val;
                    } else if (tag_type == "B") {
                        val_json = "[";
                        auto comma = tag_val.find(',');
                        if (comma != std::string::npos) {
                            std::istringstream vs(tag_val.substr(comma + 1));
                            std::string v;
                            bool first_v = true;
                            while (std::getline(vs, v, ',')) {
                                if (!first_v) val_json += ",";
                                val_json += v;
                                first_v = false;
                            }
                        }
                        val_json += "]";
                    } else {
                        val_json = json_str(tag_val);
                    }

                    tags[tag_name] = "{\"type\":" + json_str(tag_type)
                                   + ",\"value\":" + val_json + "}";
                }
            }

            rj << ",\"tags\":{";
            bool first_tag = true;
            for (auto & [k, v] : tags) {
                if (!first_tag) rj << ",";
                rj << json_str(k) << ":" << v;
                first_tag = false;
            }
            rj << "}}";

            record_jsons.push_back(rj.str());
        }
        file.close();

        // Sort comments for multiset semantics
        std::sort(co_entries.begin(), co_entries.end());

        // --- Output canonical JSON ---
        std::cout << "{\"format\":\"SAM\",\"header\":{";
        std::cout << "\"HD\":" << hd_json;

        auto print_array = [](std::vector<std::string> const & v) {
            std::cout << "[";
            for (size_t i = 0; i < v.size(); ++i) {
                if (i > 0) std::cout << ",";
                std::cout << v[i];
            }
            std::cout << "]";
        };

        std::cout << ",\"SQ\":"; print_array(sq_entries);
        std::cout << ",\"RG\":"; print_array(rg_entries);
        std::cout << ",\"PG\":"; print_array(pg_entries);

        std::cout << ",\"CO\":[";
        for (size_t i = 0; i < co_entries.size(); ++i) {
            if (i > 0) std::cout << ",";
            std::cout << json_str(co_entries[i]);
        }
        std::cout << "]";

        std::cout << "},\"records\":"; print_array(record_jsons);
        std::cout << "}" << std::endl;

        return 0;

    } catch (std::exception const & e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
