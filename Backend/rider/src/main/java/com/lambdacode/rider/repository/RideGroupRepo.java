package com.lambdacode.rider.repository;

import com.lambdacode.rider.model.RideGroup;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RideGroupRepo extends JpaRepository<RideGroup, Long> {
    Optional<RideGroup> findBygroupName(String groupName);
}
