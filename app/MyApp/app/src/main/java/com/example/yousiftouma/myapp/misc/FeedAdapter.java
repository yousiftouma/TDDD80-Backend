package com.example.yousiftouma.myapp.misc;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.example.yousiftouma.myapp.R;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * Populates feed
 */
public class FeedAdapter extends BaseAdapter {

    private ArrayList<JSONObject> feedList;
    private LayoutInflater mInflater;

    public FeedAdapter(Context context, ArrayList<JSONObject> feedList) {
        super();
        this.feedList = feedList;
        this.mInflater = LayoutInflater.from(context);
    }

    @Override
    public int getCount() {
        return feedList.size();
    }

    @Override
    public Object getItem(int position) {
        return feedList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    private class ViewHolder {
        TextView username;
        TextView title;
        TextView description;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {

        ViewHolder viewHolder;
        View view;

        if (convertView == null) {
            view = mInflater.inflate(R.layout.feed_item_layout, parent, false);
            viewHolder = new ViewHolder();
            viewHolder.username = (TextView) view.findViewById(R.id.username);
            System.out.println(viewHolder.username.getText());
            viewHolder.title = (TextView) view.findViewById(R.id.title);
            viewHolder.description = (TextView) view.findViewById(R.id.description);

            view.setTag(viewHolder);
        }

        else {
            view = convertView;
            viewHolder = (ViewHolder) view.getTag();
        }

        /**
         * Gets a JSON object containing a post, gets the data
         * from every key and sets it to the corresponding TextView
         */
        JSONObject post = feedList.get(position);
        System.out.println("hej: " + post);
        try {
            viewHolder.username.setText(post.getString("artist"));
            viewHolder.title.setText(post.getString("title"));
            viewHolder.description.setText(post.getString("description"));
        } catch (JSONException e) {
            e.printStackTrace();
            e.getMessage();
        }
        return view;
    }
}
