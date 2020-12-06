package com.example.myapplication;

import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.text.TextUtils;
import android.text.method.HideReturnsTransformationMethod;
import android.text.method.PasswordTransformationMethod;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{
    private Button button1,btn_login;
    private EditText et_user_name,et_psw;
    private String userName,psw,spPsw;
    private CustomVideoView videoview;
    private CheckBox checkBox;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
        button1 = (Button) findViewById(R.id.btn_register);//id后面为上方button的id
        btn_login = (Button) findViewById(R.id.btn_login);
        button1.setOnClickListener(new View.OnClickListener() {
                                       @Override
                                       public void onClick(View v) {

                                           Intent intent = new Intent(MainActivity.this, register.class);
                                           startActivityForResult(intent, 1);
                                       }
                                   });
        et_user_name= (EditText) findViewById(R.id.et_user_name);
        et_psw= (EditText) findViewById(R.id.et_psw);
        checkBox = findViewById(R.id.check_box);
        checkBox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {

            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // TODO Auto-generated method stub
                if(isChecked){
                    //如果选中，显示密码
                    et_psw.setTransformationMethod(HideReturnsTransformationMethod.getInstance());
                }else{
                    //否则隐藏密码
                    et_psw.setTransformationMethod(PasswordTransformationMethod.getInstance());

                }

            }
        });
        btn_login.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    //开始登录，获取用户名和密码 getText().toString().trim();
                    userName = et_user_name.getText().toString().trim();
                    psw = et_psw.getText().toString().trim();
                    //对当前用户输入的密码进行MD5加密再进行比对判断, MD5Utils.md5( ); psw 进行加密判断是否一致
                    String md5Psw = MD5Utils.toMD5(psw);
                    // md5Psw ; spPsw 为 根据从SharedPreferences中用户名读取密码
                    // 定义方法 readPsw为了读取用户名，得到密码
                    spPsw = readPsw(userName);
                    // TextUtils.isEmpty
                    if (TextUtils.isEmpty(userName)) {
                        Toast.makeText(MainActivity.this, "请输入用户名", Toast.LENGTH_SHORT).show();
                    } else if (TextUtils.isEmpty(psw)) {
                        Toast.makeText(MainActivity.this, "请输入密码", Toast.LENGTH_SHORT).show();
                        // md5Psw.equals(); 判断，输入的密码加密后，是否与保存在SharedPreferences中一致
                    } else if (md5Psw.equals(spPsw)) {
                        //一致登录成功
                        Toast.makeText(MainActivity.this, "登录成功", Toast.LENGTH_SHORT).show();
                        //保存登录状态，在界面保存登录的用户名 定义个方法 saveLoginStatus boolean 状态 , userName 用户名;
                        saveLoginStatus(true, userName);
                        //登录成功后关闭此页面进入主页
                        Intent data = new Intent();
                        //datad.putExtra( ); name , value ;
                        data.putExtra("isLogin", true);
                        //RESULT_OK为Activity系统常量，状态码为-1
                        // 表示此页面下的内容操作成功将data返回到上一页面，如果是用back返回过去的则不存在用setResult传递data值
                        setResult(RESULT_OK, data);
                        //销毁登录界面
                        MainActivity.this.finish();
                        //跳转到主界面，登录成功的状态传递到 MainActivity 中
                        startActivity(new Intent(MainActivity.this, main4.class));
                    } else if ((spPsw != null && !TextUtils.isEmpty(spPsw) && !md5Psw.equals(spPsw))) {
                        Toast.makeText(MainActivity.this, "输入的用户名和密码不一致", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(MainActivity.this, "此用户名不存在", Toast.LENGTH_SHORT).show();
                    }
                }
        });
        //透明状态栏          
    }
    private void initView() {
        videoview = (CustomVideoView) findViewById(R.id.videoview);
        videoview.setVideoURI(Uri.parse("android.resource://"+getPackageName()+"/"+R.raw.a));
        //播放
        videoview.start();
        //循环播放
        videoview.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            @Override
            public void onCompletion(MediaPlayer mediaPlayer) {
                videoview.start();
            }
        });
    }
    private String readPsw(String userName){
        //getSharedPreferences("loginInfo",MODE_PRIVATE);
        //"loginInfo",mode_private; MODE_PRIVATE表示可以继续写入
        SharedPreferences sp=getSharedPreferences("loginInfo", MODE_PRIVATE);
        //sp.getString() userName, "";
        return sp.getString(userName , "");
    }
    /**
     *保存登录状态和登录用户名到SharedPreferences中
     */
    private void saveLoginStatus(boolean status,String userName){
        //loginInfo表示文件名  SharedPreferences sp=getSharedPreferences("loginInfo", MODE_PRIVATE);
        SharedPreferences sp=getSharedPreferences("loginInfo", MODE_PRIVATE);
        //获取编辑器
        SharedPreferences.Editor editor=sp.edit();
        //存入boolean类型的登录状态
        editor.putBoolean("isLogin", status);
        //存入登录状态时的用户名
        editor.putString("loginUserName", userName);
        //提交修改
        editor.apply();
    }
    /**
     * 注册成功的数据返回至此
     * @param requestCode 请求码
     * @param resultCode 结果码
     * @param data 数据
     */
    @Override
    //显示数据， onActivityResult
    //startActivityForResult(intent, 1); 从注册界面中获取数据
    //int requestCode , int resultCode , Intent data
    // LoginActivity -> startActivityForResult -> onActivityResult();
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        //super.onActivityResult(requestCode, resultCode, data);
        super.onActivityResult(requestCode, resultCode, data);
        if(data!=null){
            //是获取注册界面回传过来的用户名
            // getExtra().getString("***");
            String userName=data.getStringExtra("userName");
            if(!TextUtils.isEmpty(userName)){
                //设置用户名到 et_user_name 控件
                et_user_name.setText(userName);
                //et_user_name控件的setSelection()方法来设置光标位置
                et_user_name.setSelection(userName.length());
            }
        }
    }

    @Override
    public void onClick(View v) {

    }
}


