package com.lambdacode.rider.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;
import java.util.List;

@Document
@Data
@AllArgsConstructor
@NoArgsConstructor
public class RideGroup {

    @Id
    private ObjectId groupId;

    @NonNull
    private String groupName;

    @NonNull
    private String groupAdmin;

//    @ManyToMany(mappedBy = "rideGroups")
//    private List<User> groupMembers;
//
//    @OneToOne
//    @JoinColumn(name = "location_destination_id") // this will create the FK column in ride_group table
//    private LocationDestinationStore locationDestination;

    @DBRef
    private List<User> groupMembers = new ArrayList<>();

    @DBRef
    private LocationDestinationStore locationDestinationStore;
}
