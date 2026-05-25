package com.ecommerce.orders.dto;

import lombok.Data;

import java.math.BigDecimal;
import java.util.Map;

/** Represents the product response received from catalog-service. */
@Data
public class ProductDTO {
    private String id;
    private String name;
    private String category;
    private BigDecimal price;
    private Integer stock;
    private Map<String, Object> attributes;
}
