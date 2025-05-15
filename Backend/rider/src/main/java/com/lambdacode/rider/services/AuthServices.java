package com.lambdacode.rider.services;

import com.lambdacode.rider.dto.CreateUserDto;
import com.lambdacode.rider.dto.LoginDto;
import com.lambdacode.rider.model.User;
import com.lambdacode.rider.repository.UserRepo;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class AuthServices {

    @Autowired
    private UserRepo userRepo;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtService jwtService;

    public String registerUser(CreateUserDto createUserDto){

        try{
        Optional<User> existingUser = userRepo.findByUsername(createUserDto.getUsername());
        if (existingUser.isPresent()){
            throw new RuntimeException("Existing user");
        }
        }catch (Exception e){
            return "Existing User";
        }

        User newUser = new User();
        //set username and email
        newUser.setUsername(createUserDto.getUsername());
        newUser.setEmail(createUserDto.getEmail());

        //encrypt password
        String password = createUserDto.getPassword();
        BCryptPasswordEncoder bCrypt = new BCryptPasswordEncoder();
        newUser.setPassword(bCrypt.encode(password));

        try {
            userRepo.save(newUser);
            return "Created";
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Failed to save user");
        }
        return null;
    }

    public String verifyUser(LoginDto loginReq) {
        Authentication authentication = authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(loginReq.getUsername(), loginReq.getPassword()));

        if (authentication.isAuthenticated()){
            return jwtService.generateToken(loginReq.getUsername());
        }
        return null;

    }
}
