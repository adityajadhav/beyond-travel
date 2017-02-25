package com.travelpro.entities;

/**
 * Created by neo on 25-02-2017.
 */

import java.text.DateFormat;
import java.util.Date;

public class TokenEntity {

    private String id;

    private String belongToUser;
    private String createdDate;

    public TokenEntity() {
        this.createdDate = DateFormat.getDateTimeInstance().format(new Date());
    }

    public String getBelongToUser() {
        return belongToUser;
    }

    public void setBelongToUser(String belongToUser) {
        this.belongToUser = belongToUser;
    }

    public String getId() {
        return id;
    }

    public String getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(String createdDate) {
        this.createdDate = createdDate;
    }

    public void setId(String id) {
        this.id = id;
    }
}
