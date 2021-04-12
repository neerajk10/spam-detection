package JavaFiles.HttpPostJsonReq.src;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

public class AppHttpPostJson {
    public static void main(String[] args) throws IOException {
        //Change the URL with any other publicly accessible POST resource, which accepts JSON request body
		URL url = new URL ("http://127.0.0.1:5000/predict");
		
		HttpURLConnection con = (HttpURLConnection)url.openConnection();
		con.setRequestMethod("POST");
		
		con.setRequestProperty("Content-Type", "application/json; utf-8");
		con.setRequestProperty("Accept", "application/json");
		
		con.setDoOutput(true);
		
		//JSON String need to be constructed for the specific resource. 
		//We may construct complex JSON using any third-party JSON libraries such as jackson or org.json
		String id = "\"1000\"";
		String number = "\"9999977777\"";
		String message_body = "\"Hi, I am in a meeting. Will call back later.\"";
		message_body = "\"URGENT! Your Mobile No 07808726822 was awarded a L2,000 Bonus Caller Prize on 02/09/03! This is our 2nd attempt to contact YOU! Call 0871-872-9758 BOX95QU\"";
		// String jsonInputString = "{\"id\": \"1000\", \"number\": \"9999977777\", \"message_body\": \"Hi, I am in a meeting. Will call back later.\"}";
		String jsonInputString = "{\"id\": " + id + ", \"number\": " + number + ", \"message_body\": "+ message_body + "}";
		
		try(OutputStream os = con.getOutputStream()){
			byte[] input = jsonInputString.getBytes("utf-8");
			os.write(input, 0, input.length);			
		}

		int code = con.getResponseCode();
		System.out.println(code);
		
		try(BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "utf-8"))){
			StringBuilder response = new StringBuilder();
			String responseLine = null;
			while ((responseLine = br.readLine()) != null) {
				response.append(responseLine.trim());
			}
			// System.out.println(response.toString());
			System.out.println("Complete response:");
			System.out.println(response.toString());
			JSONObject obj =new JSONObject(response.toString());
			// System.out.println("Printing each key:value pair");
            System.out.println("Printing <JSONObject> obj :" + obj);
			System.out.println("length of JSON obj : " + obj.length());
			System.out.println("extracted id = " + obj.get("id"));
			System.out.println("Extracted spam = " + obj.get("spam"));
		}
    }
}
