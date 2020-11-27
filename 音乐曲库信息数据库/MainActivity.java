package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.myapplication.service.UserService;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);//即activity_login.xml
        findViews();
    }
    private EditText username;
    private EditText password;
    private Button login;
    private Button register;

    private void findViews() {
        username=(EditText) findViewById(R.id.et_user_name);
        password=(EditText) findViewById(R.id.et_psw);
        login=(Button) findViewById(R.id.btn_login);
        register=(Button) findViewById(R.id.btn_register);

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String name=username.getText().toString();
                System.out.println(name);
                String pass=password.getText().toString();
                System.out.println(pass);

                Log.i("TAG",name+"_"+pass);
                UserService uService=new UserService(MainActivity.this);
                boolean flag=uService.login(name, pass);

                if(flag){
                    Log.i("TAG","登录成功");
                    Toast.makeText(MainActivity.this, "登录成功", Toast.LENGTH_LONG).show();
                    Intent intent = new Intent(MainActivity.this,register.class);
                    startActivity(intent);
                }else{
                    Log.i("TAG","登录失败");
                    Toast.makeText(MainActivity.this, "登录失败", Toast.LENGTH_LONG).show();
                }
            }
        });
        register.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(MainActivity.this,register.class);
                startActivity(intent);
            }
        });
    }
}

