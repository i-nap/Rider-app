package com.lambdacode.rider.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
public class LocationDestinationStore {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long locationId;

    private double startLongitude;
    private double startLatitude;

    private double endingLongitude;
    private double endingLatitude;

    private Long timeInitiated;

    @OneToOne
    @JoinColumn(name = "groupId")
    private RideGroup rideGroup;
}
