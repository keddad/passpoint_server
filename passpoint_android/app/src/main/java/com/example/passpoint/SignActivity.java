package com.example.passpoint;

import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class SignActivity extends AppCompatActivity {

    private static String TAG = "SignLog";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.w(TAG, "onCreate");
        setContentView(R.layout.activity_sign);
    }

    @Override
    public void onBackPressed() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    public void sendSign(View view) {

        EditText editText = findViewById(R.id.name_edittext);
        String[] name = editText.getText().toString().split(" ");

        if (name.length != 3) {
            Toast.makeText(this, "Введите полное ФИО!", Toast.LENGTH_LONG).show();
            return;
        }

        DrawingView signView = findViewById(R.id.sign);
        byte[] sign = signView.getSign();

        Send send = new Send(1, 1, name[1], name[0], name[2], sign);

        new SendTask().doInBackground(send);

        if (!isOnline()) Toast.makeText(this, "Нет интернет соединения.\nПодпись будет отправлена когда соединение появится", Toast.LENGTH_LONG).show();
        else Toast.makeText(this, "Подпись была отправлена", Toast.LENGTH_LONG).show();


        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                startActivity(intent);
                finish();
            }
        }, 100);
    }

    protected boolean isOnline() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        if (netInfo != null && netInfo.isConnected()) {
            return true;
        } else {
            return false;
        }
    }
}
