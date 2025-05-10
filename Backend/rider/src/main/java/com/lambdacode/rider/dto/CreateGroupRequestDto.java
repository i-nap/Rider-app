package com.lambdacode.rider.dto;

import lombok.Data;

@Data
public class CreateGroupRequestDto {
    private String groupName;
    private double startLongitude;
    private double startLatitude;
    private double endingLongitude;
    private double endingLatitude;
}
