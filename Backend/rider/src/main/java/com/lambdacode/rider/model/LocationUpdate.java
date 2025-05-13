package com.lambdacode.rider.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
@AllArgsConstructor
@NoArgsConstructor
@Data
public class LocationUpdate {
    @Id
    private ObjectId id;

    private Double latitude;
    private Double longitude;
    private Long timestamp;

//    @ManyToOne
//    @JoinColumn(name = "userId")
//    private User user;
//
//    @ManyToOne
//    @JoinColumn(name = "groupId")
//    private RideGroup group;

    @DBRef
    private User user;

    @DBRef
    private RideGroup group;
}
