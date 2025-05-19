package com.lambdacode.rider.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BaseResponse<T> {
    public int code;
    public String message;
    public Boolean status;
    public Object data;
}
