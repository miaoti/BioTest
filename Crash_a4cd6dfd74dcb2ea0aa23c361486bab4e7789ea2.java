import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_a4cd6dfd74dcb2ea0aa23c361486bab4e7789ea2 {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAABdwQAAAABdXIAAltCrPMX+AYIVOACAAB4cAAAAQwfiwgEAAAAAAD/BgBCQwIAcwBzcvRlnMjAwOAQHMgZ7GeVnFFkyOnjZ2VoYGDAhSQGEsAlrmuEVc4Ij5wxNrN0UCTYgI5iBWKQDMMLZgYGTigHJA0W4EUSANmDLGiEIgg1xxjM4YJq04GLAAB9gVrcBAEAAB+LCAQAAAAAAP8GAEJDAgB7ALNgQABWBk8hRiDNBcT/oQAknpxRZMiwAMgQVHJy6fgPB5ZQfXlAzIZHbxI2zTZAIZCGZCDmxKPZytDAAJt+B6AQE1Q/LwH9uka4zWAmbIYRPjNswQEHMYMLjzt0gIQxNgMAaPxfWIIBAAAfiwgEAAAAAAD/BgBCQwIAGwADAAAAAAAAAAAAeA==");

    public static void main(String[] args) throws Throwable {
        Crash_a4cd6dfd74dcb2ea0aa23c361486bab4e7789ea2.class.getClassLoader().setDefaultAssertionStatus(true);
        try {
            Method fuzzerInitialize = SAMCodecFuzzer.class.getMethod("fuzzerInitialize");
            fuzzerInitialize.invoke(null);
        } catch (NoSuchMethodException ignored) {
            try {
                Method fuzzerInitialize = SAMCodecFuzzer.class.getMethod("fuzzerInitialize", String[].class);
                fuzzerInitialize.invoke(null, (Object) args);
            } catch (NoSuchMethodException ignored1) {
            } catch (IllegalAccessException | InvocationTargetException e) {
                e.printStackTrace();
                System.exit(1);
            }
        } catch (IllegalAccessException | InvocationTargetException e) {
            e.printStackTrace();
            System.exit(1);
        }
        com.code_intelligence.jazzer.api.CannedFuzzedDataProvider input = new com.code_intelligence.jazzer.api.CannedFuzzedDataProvider(base64Bytes);
        SAMCodecFuzzer.fuzzerTestOneInput(input);
    }
}