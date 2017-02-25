package com.travelpro.services;

import android.content.SharedPreferences;
import android.util.Log;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.FirebaseInstanceIdService;
import com.google.firebase.messaging.FirebaseMessaging;
import com.travelpro.travelpro.entities.TokenEntity;

/**
 * Created by neo on 25-02-2017.
 */

public class MyFirebaseInstanceIDService extends FirebaseInstanceIdService {

    private static final String TAG = "MyFirebaseIIDService";

    private DatabaseReference mDatabase;

    @Override
    public void onTokenRefresh() {

        //Getting registration token
        String refreshedToken = FirebaseInstanceId.getInstance().getToken();

        FirebaseMessaging.getInstance().subscribeToTopic("allDevices");//Displaying token on logcat

        SharedPreferences.Editor editor = getSharedPreferences("TAHelper", MODE_PRIVATE).edit();
        editor.clear();
        editor.putString("refreshedToken", refreshedToken);
        editor.commit();
        Log.d(TAG, "Refreshed token: " + refreshedToken);
        sendRegistrationToServer(refreshedToken);
    }

    private void sendRegistrationToServer(String token) {
        mDatabase = FirebaseDatabase.getInstance().getReference();
        TokenEntity tokenEntity = new TokenEntity();
        tokenEntity.setId(token);
        mDatabase.child("token").child(token).setValue(tokenEntity);

    }
}