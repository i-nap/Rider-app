package com.lambdacode.rider.exception;

import com.lambdacode.rider.dto.response.BaseResponse;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ResponseBody
    public BaseResponse<Object> handleNotFoundException(NotFoundException ex) {
        return new BaseResponse<>(404, ex.getMessage(), false, null);
    }

    @ExceptionHandler(ForbiddenException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    @ResponseBody
    public BaseResponse<Object>  handleForbiddenException(ForbiddenException ex) {
        return new BaseResponse<>(403, ex.getMessage(), false, null);
    }

    @ExceptionHandler(ValidationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ResponseBody
    public BaseResponse<Object>  handleValidationException(ValidationException ex) {
        return new BaseResponse<>(400, ex.getMessage(), false, null);
    }

    @ExceptionHandler(ConflictException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    @ResponseBody
    public BaseResponse<Object>  handleConflictException(ConflictException ex) {
        return new BaseResponse<>(409, ex.getMessage(), false, null);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ResponseBody
    public BaseResponse<Object>  handleGenericException(Exception ex) {
        // For security, don’t expose exception message here feri database ko error ayo bhane hacker say bye bye to our system
        return new BaseResponse<>(500, "Internal Server Error", false, null);
    }
}
