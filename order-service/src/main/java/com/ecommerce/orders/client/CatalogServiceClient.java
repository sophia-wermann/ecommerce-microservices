package com.ecommerce.orders.client;

import com.ecommerce.orders.dto.ProductDTO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

@Slf4j
@Component
public class CatalogServiceClient {

    private final RestTemplate restTemplate;
    private final String catalogServiceUrl;

    public CatalogServiceClient(RestTemplate restTemplate,
                                @Value("${catalog.service.url}") String catalogServiceUrl) {
        this.restTemplate = restTemplate;
        this.catalogServiceUrl = catalogServiceUrl;
    }

    /**
     * Fetches a product from the catalog-service by ID.
     *
     * @param productId MongoDB ObjectId string
     * @return ProductDTO if found, or null if product does not exist
     */
    public ProductDTO getProduct(String productId) {
        String url = catalogServiceUrl + "/products/" + productId;
        try {
            return restTemplate.getForObject(url, ProductDTO.class);
        } catch (HttpClientErrorException.NotFound e) {
            log.warn("[CatalogServiceClient] Product not found: {}", productId);
            return null;
        } catch (Exception e) {
            log.error("[CatalogServiceClient] Failed to reach catalog-service: {}", e.getMessage());
            throw new RuntimeException("Catalog service is unavailable. Please try again later.");
        }
    }
}
