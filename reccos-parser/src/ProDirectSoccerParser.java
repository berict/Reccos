import java.io.*;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ProDirectSoccerParser {

    public static int threadCount = 512;
    public static int itemCount = 300000;

    public static int itemProcessedCount = 0;

    public static BufferedWriter bw = null;
    public static FileWriter fw = null;

    public static int finishedThreadCount = 0;

    public static void main(String[] args) {

        try {
            fw = new FileWriter("data.db");
            bw = new BufferedWriter(fw);

            // open JSON
            bw.write("{\n");

            for (int i = 1; i <= threadCount; i++) {
                new Parser(i, threadCount, itemCount, bw, fw, new Runnable() {
                    @Override
                    public void run() {
                        finish();
                    }
                }).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
        }
    }

    private static void finish() {
        ++finishedThreadCount;

        if (threadCount == finishedThreadCount) {
            try {
                if (bw != null) {
                    // close JSON
                    bw.write("\n}");
                    bw.close();
                }
                if (fw != null) {
                    fw.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
}

class Parser extends Thread {

    private int id;

    private int threadCount;
    private int itemCount;

    private BufferedWriter bw = null;
    private FileWriter fw = null;

    private URL u;
    private InputStream is = null;
    private DataInputStream dis;
    private String s;

    private Runnable onFinish;

    public Parser(int id, int threadCount, int itemCount, BufferedWriter bw, FileWriter fw, Runnable onFinish) {
        this.id = id;
        this.threadCount = threadCount;
        this.itemCount = itemCount;
        this.bw = bw;
        this.fw = fw;
        this.onFinish = onFinish;
    }

    @Override
    public void run() {
        System.out.println("Started thread id " + id);
        get(id);
    }

    private void get(int id) {
        try {
            u = new URL("http://www.prodirectsoccer.com/products/" + id + ".aspx");

            is = u.openStream();
            dis = new DataInputStream(new BufferedInputStream(is));

            StringBuilder result = new StringBuilder();

            boolean isInDescription = false;
            boolean isInGroundType = false;

            while ((s = dis.readLine()) != null) {
                if (s.contains("http://www.prodirectsoccer.com/404.aspx")) {
                    // no product
                    result = null;
                    break;
                }

                if (s.contains("addProduct")) {
                    Pattern pattern = Pattern.compile("\\{(.+)\\}");
                    Matcher matcher = pattern.matcher(s);
                    matcher.find();
                    result.append("{").append(matcher.group(1));
                }

                if (s.contains("itemprop=\"description\"")) {
                    isInDescription = true;
                    result.append("'description': ");
                    result.append("'");
                    continue;
                }

                if (isInDescription) {
                    // description
                    if (s.contains("</div>")) {
                        result.append("',");
                        isInDescription = false;
                    } else {
                        // the content
                        result.append(s.trim());
                    }
                }

                if (s.contains("class=\"ground-icon")) {
                    // ground type
                    isInGroundType = true;
                    result.append("'groundType': ");
                    result.append("'");
                    continue;
                }

                if (isInGroundType) {
                    if (s.contains("<ul>")) {
                        result.append("',");
                        isInGroundType = false;
                    } else if (s.contains("h4")) {
                        // the content
                        result.append(s.substring(4, s.length() - 5));
                    }
                }

                if (s.contains("itemprop=\"mpn\"")) {
                    // manual product number
                    result.append("'mpn': '");
                    result.append(s.substring(s.indexOf("\"mpn\">") + 6, s.lastIndexOf("</span>") - 1));
                    result.append("',");
                }
            }

            result.append("}");

            System.out.println(result);

            try {
                bw.write(result.toString());
                bw.write(",\n");
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
        } finally {
            try {
                is.close();
            } catch (Exception e) {
            }

            if (id + threadCount <= itemCount) {
                get(id + threadCount);
            } else {
                System.out.println("Finished thread id " + id);
                onFinish.run();
            }
        }
    }
}
