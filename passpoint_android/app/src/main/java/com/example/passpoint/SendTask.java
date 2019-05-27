package com.example.passpoint;

import android.os.AsyncTask;
import android.util.Log;

import com.google.gson.Gson;

import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class SendTask extends AsyncTask<Send, Void, Void> {
    private static String TAG = "AsyncSendLog";
    private static String ip = "81.23.11.22";

    @Override
    protected Void doInBackground(Send... sends) {
        Send send = sends[0];

        Gson gson = new Gson();

        Log.w(TAG, gson.toJson(send).toString());

        try {

            URL url = new URL(ip);

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");

            String jsonObject = gson.toJson(send);

            // 3. add JSON content to POST request body
            setPostRequestContent(conn, jsonObject);

            // 4. make POST request to the given URL
            conn.connect();
        } catch (IOException e) {
            Log.e(TAG, e.getMessage());
        }

        return null;
    }

    private void setPostRequestContent(HttpURLConnection conn,
                                       String jsonObject) throws IOException {

        OutputStream os = conn.getOutputStream();
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
        writer.write(jsonObject);
        writer.flush();
        writer.close();
        os.close();
    }
}
