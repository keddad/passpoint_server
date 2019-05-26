package com.example.passpoint;

import android.content.Intent;
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

    public void sendSign(View view) {
        EditText editText = findViewById(R.id.name_edittext);
        String name = editText.getText().toString();
        DrawView drawView = findViewById(R.id.sign);
        byte[] sign = drawView.getSign();

        Toast.makeText(this, "Sign has been sent to server", Toast.LENGTH_LONG).show();
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }
}
