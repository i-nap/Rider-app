package com.lambdacode.rider.repository;

import com.lambdacode.rider.model.RideGroup;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface RideGroupRepo extends MongoRepository<RideGroup, ObjectId> {
    Optional<RideGroup> findBygroupName(String groupName);
}
