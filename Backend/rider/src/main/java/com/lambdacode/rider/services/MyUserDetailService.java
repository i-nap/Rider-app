package com.lambdacode.rider.services;

import com.lambdacode.rider.model.User;
import com.lambdacode.rider.model.UserPrincipal;
import com.lambdacode.rider.repository.UserRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class MyUserDetailService implements UserDetailsService {

    @Autowired
    private UserRepo userRepo;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Optional<User> user = userRepo.findByUsername(username);
        if (user.isEmpty()) {
            System.out.println("user not found");
            throw new UsernameNotFoundException("User not found");
        }

        User foundUser = user.get();

        return new UserPrincipal(foundUser);
    }
}
