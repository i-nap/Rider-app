package com.lambdacode.rider.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Document
@Data
@AllArgsConstructor
@NoArgsConstructor
public class LocationDestinationStore {

    @Id
    private ObjectId locationId;

    private double startLongitude;
    private double startLatitude;

    private double endingLongitude;
    private double endingLatitude;

    private LocalDateTime timeInitiated;

//    @OneToOne(mappedBy = "locationDestination")
//    private RideGroup rideGroup;

    @DBRef
    private RideGroup rideGroup;

}
