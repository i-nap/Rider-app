package com.lambdacode.rider.repository;

import com.lambdacode.rider.model.LocationDestinationStore;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface LocationDestiStoreRepo extends MongoRepository<LocationDestinationStore, ObjectId> {

}
