import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.InputStream;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class FootballBootsDatabaseParser {

    private static int threadCount = 32;

    public static void main(String[] args) {
        for (int i = 1; i <= threadCount; i++) {
            final int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    get(finalI);
                }
            }).start();
        }
    }

    static void get(int id) {
        URL u;
        InputStream is = null;
        DataInputStream dis;
        String s;

        try {
            u = new URL("http://www.footballbootsdb.com/boot/-/" + id);

            is = u.openStream();
            dis = new DataInputStream(new BufferedInputStream(is));

            boolean print = false;

            while ((s = dis.readLine()) != null) {
                if (s.contains("<div class=\"top-info\">")) {
                    print = true;
                }

                if (s.contains("<style>")) {
                    print = false;
                }

                if (print) {
                    if (s.contains("h1")) {
                        Pattern pattern = Pattern.compile(">(.+)<");
                        Matcher matcher = pattern.matcher(s);
                        matcher.find();
                        System.out.println("Name : " + matcher.group(1));
                    }

                    if (s.contains("<p>")) {
                        Pattern pattern = Pattern.compile(">(.+)<");
                        Matcher matcher = pattern.matcher(s);
                        matcher.find();
                        System.out.println("Desc : " + matcher.group(1));
                    }
                }
            }

        } catch (Exception e) {
            System.out.println("Error: request failed on id  " + id);
        } finally {
            try {
                is.close();
            } catch (Exception e) {}

            if (id + threadCount <= 227) {
                get(id + threadCount);
            }
        }
    }
}
