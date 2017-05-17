package com.wizards.data.datawizards;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class Confirm extends AppCompatActivity implements View.OnClickListener {

    //URL to get JSON Array
    private static String url = "http://api.androidhive.info/contacts/";

    //JSON Node Names
    private static final String TAG_TRANS = "contacts";
    private static final String TAG_RESULTS = "id";
    private static final String TAG_MESSAGE = "name";
    ArrayList<HashMap<String, String>> transactions;

    JSONArray transaction = null;
    private boolean isRejected = false;
    JSONParser jParser = new JSONParser();
    private JSONObject jsonObject;
    private JSONObject c;
    private Button btnConfirm, btnReject, btnExit;
    private TextView tvDisplay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.confirm);
        initialize();

        new JSONParse().execute();

        if (jsonObject!=null) {
            btnConfirm.setVisibility(View.VISIBLE);
            btnReject.setVisibility(View.VISIBLE);
            btnExit.setVisibility(View.GONE);
        } else {
            btnConfirm.setVisibility(View.GONE);
            btnReject.setVisibility(View.GONE);
            btnExit.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.btnConfirm:
                //TODO sends information(confirm) back to the engine
                new JSONParse().execute();
                break;
            case R.id.btnReject:
                //TODO sends information(reject) back to the engine
                isRejected = true;
                new JSONParse().execute();
                break;
            case R.id.btnCancel:
                onBackPressed();
            default:
                break;
        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
    }

    void initialize() {
        btnConfirm = (Button) findViewById(R.id.btnConfirm);
        btnReject = (Button) findViewById(R.id.btnReject);
        btnExit = (Button) findViewById(R.id.btnCancel);
        tvDisplay = (TextView) findViewById(R.id.tvDisplayInfo);
        transactions = new ArrayList<HashMap<String, String>>();

        btnReject.setOnClickListener(this);
        btnConfirm.setOnClickListener(this);
        btnExit.setOnClickListener(this);
    }

    private class JSONParse extends AsyncTask<Void, Void, Void> {
        private ProgressDialog _dialog;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            _dialog = new ProgressDialog(Confirm.this);
            _dialog.setMessage("Sending response ...");
            _dialog.setCancelable(true);
            _dialog.show();
        }

        @Override
        protected Void doInBackground(Void... args) {

            // Getting JSON from URL
            jsonObject = new JSONObject();
            if(!isRejected)
            {
                String jsonStr = jParser.makeService(url, JSONParser.GET);
                HashMap<String, String> tr = new HashMap<>();
                if (jsonStr != null) {
                    try{
                        JSONObject jsonObj = new JSONObject(jsonStr);
                        // Getting JSON Array node
                        transaction = jsonObj.getJSONArray(TAG_TRANS);
                        c = transaction.getJSONObject(0);
                        tr.put(TAG_MESSAGE, c.getString(TAG_MESSAGE));
                        tr.put(TAG_RESULTS, c.getString(TAG_RESULTS));
                        transactions.add(tr);

                    }catch (Exception e)
                    {
                        e.printStackTrace();
                    }
                } else {
                    Log.e("ServiceHandler", "Couldn't get any data from the url");
                }
            }else {
                String jsonStr = jParser.makeService(url, JSONParser.POST);
                HashMap<String, String> tr = new HashMap<>();
                if (jsonStr != null) {
                    try{
                        JSONObject jsonObj = new JSONObject(jsonStr);
                        // Getting JSON Array node
                        transaction = jsonObj.getJSONArray(TAG_TRANS);
                        c = transaction.getJSONObject(0);
                        tr.put(TAG_MESSAGE, c.getString(TAG_MESSAGE));
                        tr.put(TAG_RESULTS, c.getString(TAG_RESULTS));
                        transactions.add(tr);

                    }catch (Exception e)
                    {
                        e.printStackTrace();
                    }
                } else {
                    Log.e("ServiceHandler", "Couldn't get any data from the url");
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void json) {
            if (_dialog.isShowing())
                _dialog.dismiss();
            try {
                tvDisplay.setText(c.getString(TAG_MESSAGE));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
