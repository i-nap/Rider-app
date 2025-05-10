package com.lambdacode.rider.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
public class RideGroup {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long groupId;

    @Column(nullable = false)
    private String groupName;

    @Column(nullable = false)
    private String groupAdmin;

    @ManyToMany(mappedBy = "rideGroups")
    private List<User> groupMembers;

    @OneToOne
    @JoinColumn(name = "location_destination_id") // this will create the FK column in ride_group table
    private LocationDestinationStore locationDestination;

}
