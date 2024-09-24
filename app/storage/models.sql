-- Таблица для хранения источников данных
CREATE TABLE listing_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,         
    base_url VARCHAR(255) NOT NULL      
);

-- Таблица для хранения объявлений
CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,        
    description TEXT,                   
    price NUMERIC(10, 2) NOT NULL,      
    deal_type VARCHAR(50) NOT NULL,     
    rooms INT,                          
    area NUMERIC(10, 2),                
    location VARCHAR(255),              
    created_at TIMESTAMP DEFAULT NOW(), 
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id)
);

-- Таблица для хранения данных с разных источников по каждому объявлению
CREATE TABLE listing_prices (
    id SERIAL PRIMARY KEY,
    listing_id INT NOT NULL,             
    source_id INT NOT NULL,              
    price NUMERIC(10, 2),                
    source_url VARCHAR(255) NOT NULL,    
    last_checked TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES listing_sources(id) ON DELETE CASCADE
);

-- Таблица для хранения данных аналитики (например, изменение цены, популярность объявлений)
CREATE TABLE listing_analytics (
    id SERIAL PRIMARY KEY,
    listing_id INT NOT NULL,             
    source_id INT NOT NULL,              
    price NUMERIC(10, 2),                
    recorded_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES listing_sources(id) ON DELETE CASCADE
);

-- Таблица для хранения категорий или типов недвижимости
CREATE TABLE property_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Таблица для связывания объявлений с категориями недвижимости
CREATE TABLE listing_property_types (
    listing_id INT NOT NULL,
    property_type_id INT NOT NULL,
    PRIMARY KEY (listing_id, property_type_id),
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (property_type_id) REFERENCES property_types(id) ON DELETE CASCADE
);
