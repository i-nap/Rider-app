package com.lambdacode.rider.services;

import com.lambdacode.rider.dto.CreateGroupRequestDto;
import com.lambdacode.rider.model.LocationDestinationStore;
import com.lambdacode.rider.model.RideGroup;
import com.lambdacode.rider.repository.LocationDestiStoreRepo;
import com.lambdacode.rider.repository.RideGroupRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class GroupServices {

    @Autowired
    private RideGroupRepo rideGroupRepo;

    @Autowired
    private LocationDestiStoreRepo locationDestiStoreRepo;

    public Boolean createGroup(CreateGroupRequestDto request, String username) {
        RideGroup createGroup = new RideGroup();
        createGroup.setGroupName(request.getGroupName());
        createGroup.setGroupAdmin(username);

        RideGroup savedGroup = rideGroupRepo.save(createGroup);

        LocationDestinationStore destinationStore =new LocationDestinationStore();
        destinationStore.setStartLatitude(request.getStartLatitude());
        destinationStore.setStartLongitude(request.getStartLongitude());
        destinationStore.setEndingLatitude(request.getEndingLatitude());
        destinationStore.setEndingLongitude(request.getEndingLongitude());
        destinationStore.setTimeInitiated(System.currentTimeMillis());
        destinationStore.setRideGroup(createGroup);

        LocationDestinationStore savedLocation = locationDestiStoreRepo.save(destinationStore);

        savedGroup.setLocationDestination(savedLocation);
        rideGroupRepo.save(savedGroup);

        return true;

    }
}
