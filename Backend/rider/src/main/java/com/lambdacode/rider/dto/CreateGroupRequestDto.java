package com.lambdacode.rider.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class CreateGroupRequestDto {
    private String groupName;
    private double startLongitude;
    private double startLatitude;
    private double endingLongitude;
    private double endingLatitude;
}
