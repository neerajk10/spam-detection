import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;
import org.json.JSONArray;

public class AppHttpPostJson {
    public static void main(String[] args) throws IOException {
        //Change the URL with any other publicly accessible POST resource, which accepts JSON request body
		URL url = new URL ("http://192.168.1.102:5000/predict");
		
		HttpURLConnection con = (HttpURLConnection)url.openConnection();
		con.setRequestMethod("POST");
		
		con.setRequestProperty("Content-Type", "application/json; utf-8");
		con.setRequestProperty("Accept", "application/json");
		
		con.setDoOutput(true);
		
		//JSON String need to be constructed for the specific resource. 
		//We may construct complex JSON using any third-party JSON libraries such as jackson or org.json
		// String id = "\"1000\"";
		String id = "1000";
		String[] message_body = new String[5];
		message_body[0] = "Hi, I am in a meeting. Will call back later.";
		message_body[1] = "IMPORTANT - You could be entitled up to £3,160 in compensation from mis-sold PPI on a credit card or loan. Please reply PPI for info or STOP to opt out.";
		message_body[2] = "A [redacted] loan for £950 is approved for you if you receive this SMS. 1 min verification & cash in 1 hr at www.[redacted].co.uk to opt out reply stop";
		message_body[3] = "You have still not claimed the compensation you are due for the accident you had. To start the process please reply YES. To opt out text STOP";
		message_body[4] = "Our records indicate your Pension is under performing to see higher growth and up to 25% cash release reply PENSION for a free review. To opt out reply STOP";
		// String number = "\"9999977777\"";
	    	
// 	    	-------------------------------------------------------------------------
	    	//this is the message string that will be tested in the DMM. Since it is statically assigned, you have to recompile the java file everytime after changing the string.
		// String message_body = "\"Hi, I am in a meeting. Will call back later.\"";
		// message_body = "\"URGENT! Your Mobile No 07808726822 was awarded a L2,000 Bonus Caller Prize on 02/09/03! This is our 2nd attempt to contact YOU! Call 0871-872-9758 BOX95QU\"";
// 		-------------------------------------------------------------------------

		JSONArray ja = new JSONArray();
		
		for(int i=0; i<5; i++){
			JSONObject jo = new JSONObject();
			Integer idint = Integer.parseInt(id) + i;
			jo.put("id", String.valueOf(idint));
			jo.put("message_body", message_body[i]);
			ja.put(jo);
		}

		JSONObject mainObj = new JSONObject();
		mainObj.put("entries", ja);
		
		String jsonInputString = mainObj.toString();
		
		System.out.println("Printing json main object");
		System.out.println(jsonInputString);

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
			
			JSONArray result_ja = (JSONArray) obj.get("result");
			System.out.println("Printing <JSONOArray> result_ja :" + result_ja);
			System.out.println("length of result_ja : " + result_ja.length());
			System.out.println("looping through the json array ");

			for(int i=0; i<result_ja.length(); i++){
				JSONObject tempjo = (JSONObject) result_ja.get(i);
				System.out.printf("[%d]  %s\n", i, tempjo.toString());
			}

			// System.out.println("extracted id = " + obj.get("id"));
			// System.out.println("Extracted spam = " + obj.get("spam"));
		}
    }
}
