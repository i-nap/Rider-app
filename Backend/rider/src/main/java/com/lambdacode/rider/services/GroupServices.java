package com.lambdacode.rider.services;

import com.lambdacode.rider.dto.CreateGroupRequestDto;
import com.lambdacode.rider.model.LocationDestinationStore;
import com.lambdacode.rider.model.RideGroup;
import com.lambdacode.rider.model.User;
import com.lambdacode.rider.repository.LocationDestiStoreRepo;
import com.lambdacode.rider.repository.RideGroupRepo;
import com.lambdacode.rider.repository.UserRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.query.Collation;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class GroupServices {

    @Autowired
    private RideGroupRepo rideGroupRepo;

    @Autowired
    private LocationDestiStoreRepo locationDestiStoreRepo;

    @Autowired
    private UserRepo userRepo;

    public Boolean createGroup(CreateGroupRequestDto request, String username) {
        RideGroup createGroup = new RideGroup();

        //creates group with name and admin
        createGroup.setGroupName(request.getGroupName());
        createGroup.setGroupAdmin(username);

        //save group name and admin in ride_group collection
        RideGroup savedGroup = rideGroupRepo.save(createGroup);

        //set location start and end location time initiated and ride group ref
        LocationDestinationStore destinationStore =new LocationDestinationStore();
        destinationStore.setStartLatitude(request.getStartLatitude());
        destinationStore.setStartLongitude(request.getStartLongitude());
        destinationStore.setEndingLatitude(request.getEndingLatitude());
        destinationStore.setEndingLongitude(request.getEndingLongitude());
        destinationStore.setTimeInitiated(LocalDateTime.now());
        destinationStore.setRideGroup(createGroup);

        //saving the data in location store collection
        LocationDestinationStore savedLocation = locationDestiStoreRepo.save(destinationStore);

        //save the location destination in the rideGroup collection
        savedGroup.setLocationDestinationStore(savedLocation);
        rideGroupRepo.save(savedGroup);

        Optional<User> foundUser = userRepo.findByUsername(username);

        if (foundUser.isPresent()) {
            User activeUser = foundUser.get();

            List<RideGroup> currentGroups = activeUser.getRideGroups();
            if (currentGroups == null) {
                currentGroups = new ArrayList<>();
            }
            currentGroups.add(savedGroup);
            activeUser.setRideGroups(currentGroups);

            userRepo.save(activeUser);
            return true;
        }

        return false;

    }
}
