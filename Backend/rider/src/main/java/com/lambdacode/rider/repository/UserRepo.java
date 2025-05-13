package com.lambdacode.rider.repository;

import com.lambdacode.rider.model.User;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.query.Collation;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface UserRepo extends MongoRepository<User, ObjectId> {
    Optional<User> findByUsername(String username);
}
