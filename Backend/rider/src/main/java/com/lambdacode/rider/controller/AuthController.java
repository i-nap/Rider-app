package com.lambdacode.rider.controller;

import com.lambdacode.rider.dto.CreateUserDto;
import com.lambdacode.rider.dto.LoginDto;
import com.lambdacode.rider.services.AuthServices;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthServices authServices;

    @PostMapping("/register")
    public ResponseEntity<?> createUser(@RequestBody CreateUserDto createUserDto){

        String createdUserResp = authServices.registerUser(createUserDto);

        if (createdUserResp.equals("Created")){
            return ResponseEntity.ok("User Created Successfully");
        }else if (createdUserResp.equals("Existing User")){
            return ResponseEntity.badRequest().body("Username Taken Login or set different Username");
        }else {
            return ResponseEntity.badRequest().body("Failed User creation");
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginDto loginReq){
        String token = authServices.verifyUser(loginReq);

        if(token != null){
           return ResponseEntity.ok("User token: " + token);
        }else {
            return ResponseEntity.status(404).body("Username or Password incorrect");
        }
    }
}
