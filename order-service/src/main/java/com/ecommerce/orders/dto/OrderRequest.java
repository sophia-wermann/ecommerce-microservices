package com.ecommerce.orders.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

import java.util.List;

@Data
public class OrderRequest {

    @NotBlank(message = "Customer name is required.")
    private String customerName;

    @NotBlank(message = "Customer email is required.")
    @Email(message = "Customer email must be valid.")
    private String customerEmail;

    @NotEmpty(message = "Order must contain at least one item.")
    @Valid
    private List<OrderItemRequest> items;
}
