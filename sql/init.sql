-- Initialize database for Affiliate Marketing Website Generator
-- This script sets up tables for storing generated website metadata and analytics

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table for storing generated websites metadata
CREATE TABLE IF NOT EXISTS generated_websites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_name VARCHAR(255) NOT NULL UNIQUE,
    brand_name VARCHAR(255) NOT NULL,
    niche VARCHAR(100) NOT NULL,
    target_audience TEXT,
    color_scheme VARCHAR(50),
    google_sheets_id VARCHAR(255),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    file_count INTEGER DEFAULT 0,
    deployment_url VARCHAR(500),
    lighthouse_score JSONB,
    performance_metrics JSONB,
    conversion_goals TEXT[],
    features TEXT[],
    status VARCHAR(50) DEFAULT 'generated',
    metadata JSONB
);

-- Table for storing research results cache
CREATE TABLE IF NOT EXISTS research_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_hash VARCHAR(64) NOT NULL UNIQUE,
    query_text TEXT NOT NULL,
    niche VARCHAR(100),
    focus_area VARCHAR(50),
    findings JSONB,
    sources TEXT[],
    recommendations JSONB,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    hits INTEGER DEFAULT 0
);

-- Table for storing generation analytics
CREATE TABLE IF NOT EXISTS generation_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    website_id UUID REFERENCES generated_websites(id) ON DELETE CASCADE,
    generation_time_seconds INTEGER,
    research_time_seconds INTEGER,
    file_generation_time_seconds INTEGER,
    validation_time_seconds INTEGER,
    total_files_generated INTEGER,
    total_research_sources INTEGER,
    error_count INTEGER DEFAULT 0,
    warnings_count INTEGER DEFAULT 0,
    success BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    ip_address INET,
    metadata JSONB
);

-- Table for storing template usage statistics
CREATE TABLE IF NOT EXISTS template_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_name VARCHAR(255) NOT NULL,
    template_type VARCHAR(100) NOT NULL, -- component, page, config, etc.
    niche VARCHAR(100),
    usage_count INTEGER DEFAULT 1,
    last_used TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    success_rate DECIMAL(5,2) DEFAULT 100.00,
    average_generation_time DECIMAL(8,2),
    metadata JSONB
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_generated_websites_niche ON generated_websites(niche);
CREATE INDEX IF NOT EXISTS idx_generated_websites_created_at ON generated_websites(generated_at);
CREATE INDEX IF NOT EXISTS idx_generated_websites_status ON generated_websites(status);

CREATE INDEX IF NOT EXISTS idx_research_cache_query_hash ON research_cache(query_hash);
CREATE INDEX IF NOT EXISTS idx_research_cache_niche ON research_cache(niche);
CREATE INDEX IF NOT EXISTS idx_research_cache_expires_at ON research_cache(expires_at);

CREATE INDEX IF NOT EXISTS idx_generation_analytics_website_id ON generation_analytics(website_id);
CREATE INDEX IF NOT EXISTS idx_generation_analytics_created_at ON generation_analytics(created_at);
CREATE INDEX IF NOT EXISTS idx_generation_analytics_success ON generation_analytics(success);

CREATE INDEX IF NOT EXISTS idx_template_usage_template_name ON template_usage(template_name);
CREATE INDEX IF NOT EXISTS idx_template_usage_niche ON template_usage(niche);
CREATE INDEX IF NOT EXISTS idx_template_usage_last_used ON template_usage(last_used);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_generated_websites_updated_at 
    BEFORE UPDATE ON generated_websites 
    FOR EACH ROW 
    EXECUTE PROCEDURE update_updated_at_column();

-- Function to clean expired research cache
CREATE OR REPLACE FUNCTION clean_expired_research_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM research_cache WHERE expires_at < CURRENT_TIMESTAMP;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ language 'plpgsql';

-- Insert some sample data for development
INSERT INTO generated_websites (
    project_name, brand_name, niche, target_audience, 
    color_scheme, google_sheets_id, file_count, 
    conversion_goals, features, status
) VALUES 
(
    'techdeals-pro', 'TechDeals Pro', 'tech', 
    'Tech enthusiasts seeking the best deals on electronics',
    'blue', '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms', 12,
    ARRAY['maximize_clicks', 'build_trust', 'increase_engagement'],
    ARRAY['responsive_design', 'seo_optimized', 'conversion_focused'],
    'generated'
),
(
    'fashion-hub', 'Fashion Hub', 'fashion',
    'Fashion-forward individuals looking for trendy apparel',
    'purple', 'sample_fashion_sheet_id', 15,
    ARRAY['build_trust', 'improve_mobile_experience'],
    ARRAY['responsive_design', 'accessibility_focused'],
    'generated'
) ON CONFLICT (project_name) DO NOTHING;

INSERT INTO template_usage (
    template_name, template_type, niche, usage_count, 
    success_rate, average_generation_time
) VALUES 
('ProductCard', 'component', 'tech', 1, 100.00, 1.2),
('Hero', 'component', 'tech', 1, 100.00, 0.8),
('Navigation', 'component', 'tech', 1, 100.00, 0.5),
('index', 'page', 'tech', 1, 100.00, 2.1),
('category/[slug]', 'page', 'tech', 1, 100.00, 1.8),
('ProductCard', 'component', 'fashion', 1, 100.00, 1.1),
('Hero', 'component', 'fashion', 1, 100.00, 0.9)
ON CONFLICT DO NOTHING;

-- Create a view for website analytics dashboard
CREATE OR REPLACE VIEW website_analytics_dashboard AS
SELECT 
    gw.project_name,
    gw.brand_name,
    gw.niche,
    gw.generated_at,
    gw.file_count,
    gw.deployment_url,
    gw.lighthouse_score,
    ga.generation_time_seconds,
    ga.total_files_generated,
    ga.total_research_sources,
    ga.success,
    ga.error_count,
    ga.warnings_count
FROM generated_websites gw
LEFT JOIN generation_analytics ga ON gw.id = ga.website_id
ORDER BY gw.generated_at DESC;

-- Grant permissions (adjust as needed for your security requirements)
-- Note: In production, create specific users with limited permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO postgres;

-- Log the successful initialization
INSERT INTO generation_analytics (
    generation_time_seconds, total_files_generated, 
    total_research_sources, success, metadata
) VALUES (
    0, 0, 0, true, 
    '{"event": "database_initialized", "timestamp": "' || CURRENT_TIMESTAMP || '"}'
);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully!';
    RAISE NOTICE 'Tables created: generated_websites, research_cache, generation_analytics, template_usage';
    RAISE NOTICE 'Views created: website_analytics_dashboard';
    RAISE NOTICE 'Sample data inserted for development';
END $$;