package com.lambdacode.rider.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateGroupRequestDto {
    private String groupName;
    private double startLongitude;
    private double startLatitude;
    private double endingLongitude;
    private double endingLatitude;
}
