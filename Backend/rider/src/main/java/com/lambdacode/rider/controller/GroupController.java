package com.lambdacode.rider.controller;

import com.lambdacode.rider.dto.CreateGroupRequestDto;
import com.lambdacode.rider.services.GroupServices;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GroupController {

    @Autowired
    private GroupServices groupServices;

    @PostMapping("/create_group/{username}")
    public ResponseEntity<?> createGroup(@RequestBody CreateGroupRequestDto request, @PathVariable String username){

        Boolean createdGroup = groupServices.createGroup(request, username);
        if(createdGroup){
            return ResponseEntity.ok("Group Created");
        }else{
            return ResponseEntity.status(400).body("Group Creation Failed");
        }


    }
}
