package com.lambdacode.rider.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;
import java.util.List;
//abcx
@Document(collection = "users")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class User {

    @Id
    private ObjectId userId;

    @NonNull
    private String username;
    @NonNull
    @Indexed(unique = true)
    private String email;
    @NonNull
    private String password;

//    @ManyToMany
//    @JoinTable(name = "joinedGroup", joinColumns = @JoinColumn(name = "userId"),inverseJoinColumns = @JoinColumn(name = "groupId"))
//    private List<RideGroup> rideGroups;

    @DBRef
    private List<RideGroup> rideGroups;
}
