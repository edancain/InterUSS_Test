-- Only create the PostGIS extension if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis') THEN
        CREATE EXTENSION postgis;
    END IF;
END
$$;


CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,  -- Make username unique
  password TEXT
);

INSERT INTO users(username, password) VALUES
 ('TestUser1', 'OneTwoThree'),
 ('TestUser2', 'OneTwoThree'),
 ('TestUser3', 'ThreeTwoOne')
 ON CONFLICT (username) DO NOTHING;

/*
CREATE TABLE IF NOT EXISTS extents (
  id UUID PRIMARY KEY,
  geom GEOMETRY,  -- Geometry column to store point (for circle) or polygon
  radius DOUBLE PRECISION,  -- Radius for circular extents, null for polygons
  altitude_lower INTEGER,
  altitude_upper INTEGER
);


-- Subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
  id UUID PRIMARY KEY,
  version TEXT, -- String, version of the subscription.
  notification_index INTEGER, -- Integer, tracks notifications sent for the subscription.
  time_start TIMESTAMP WITH TIME ZONE,
  time_end TIMESTAMP WITH TIME ZONE,
  uss_base_url TEXT, -- String, base URL of the USS.
  notify_for_operational_intents BOOLEAN, -- Boolean, flag to trigger notifications for operational intents.
  notify_for_constraints BOOLEAN, -- Boolean, flag to trigger notifications for constraints.
  implicit_subscription BOOLEAN, -- indicating if the subscription is implicit.
  dependent_operational_intents JSONB -- Use JSONB for JSON data
  );


-- Operational Intent table
CREATE TABLE IF NOT EXISTS OperationalIntents (
    id UUID PRIMARY KEY,
    manager VARCHAR(255),
    uss_availability VARCHAR(255)  CHECK (uss_availability IN ('Unknown', 'Accepted', 'Test2')),
    version INT NOT NULL,
    state VARCHAR(255) CHECK (state IN ('Accepted', 'Activated', 'Nonconforming', 'Contingent')),
    ovn UUID,
    time_start TIMESTAMPTZ NOT NULL,
    time_end TIMESTAMPTZ NOT NULL,
    uss_base_url VARCHAR(255),
    subscription_id UUID REFERENCES subscriptions(id),
    priority INT NOT NULL
);


-- Create Telemetry Table
CREATE TABLE Telemetry (
    telemetry_id SERIAL PRIMARY KEY,
    operational_intent_id UUID REFERENCES OperationalIntents(id),
    time_measured TIMESTAMPTZ,
    longitude FLOAT,
    latitude FLOAT,
    accuracy_h VARCHAR(255),
    accuracy_v VARCHAR(255),
    extrapolated BOOLEAN,
    altitude_value FLOAT,
    altitude_reference VARCHAR(255),
    altitude_units VARCHAR(255),
    velocity_speed FLOAT,
    velocity_units_speed VARCHAR(255),
    velocity_track FLOAT
);

---
--- SELECT * 
--- FROM Time 
--- WHERE associated_id = [specific_operational_intent_id] 
--- AND associated_type = 'Volume';

CREATE TABLE Time (
    associated_id UUID NOT NULL,
    associated_type VARCHAR(255) NOT NULL,
    time_start TIMESTAMPTZ,
    time_end TIMESTAMPTZ,
    PRIMARY KEY (associated_id, associated_type)
);
--- INSERT INTO Time (associated_id, associated_type, time_start, time_end)
--- VALUES 
---     (
---         'your_associated_entity_id', -- Replace with the actual ID of the associated entity
---         'Volume', -- or 'OperationalIntent', depending on the context
---         '1985-04-12T23:20:50.52Z', -- time_start value from the JSON
---         '1985-04-12T23:20:50.52Z' -- time_end value from the JSON
---     );


--- PostgreSQL stores date and time values in a standardized internal format. When you use a data type 
--- like TIMESTAMPTZ (timestamp with time zone), PostgreSQL automatically handles the formatting and parsing according to international standards (which includes RFC 3339).

CREATE TABLE Volume (
    volume_id SERIAL PRIMARY KEY,
    parent_id UUID NOT NULL,
    parent_type TEXT NOT NULL,
    altitude_lower_value FLOAT,
    altitude_lower_reference VARCHAR(255),
    altitude_lower_units VARCHAR(255),
    altitude_upper_value FLOAT,
    altitude_upper_reference VARCHAR(255),
    altitude_upper_units VARCHAR(255)
);

--- Handling Relationships in Queries
--- When querying the Volume table, you'll need to join it with either the OperationalIntent table or the Constraint table based on the parent_type. Here's an example SQL query to fetch volumes associated with an operational intent:

--- sql
--- SELECT *
--- FROM Volume
--- JOIN OperationalIntent ON Volume.parent_id = OperationalIntent.id
--- WHERE Volume.parent_type = 'OperationalIntent';

--- SELECT *
--- FROM Volume
--- JOIN Constraint ON Volume.parent_id = Constraint.id
--- WHERE Volume.parent_type = 'Constraint';


CREATE TABLE Circle (
    circle_id SERIAL PRIMARY KEY,
    volume_id INT REFERENCES Volume(volume_id),
    center_lng DOUBLE PRECISION,  
    center_lat FLOAT,
    radius_value FLOAT,
    radius_units VARCHAR(255)
);


CREATE TABLE Polygon (
    polygon_id SERIAL PRIMARY KEY,
    volume_id INT REFERENCES Volume(volume_id)
);


CREATE TABLE Vertex (
    vertex_id SERIAL PRIMARY KEY,
    polygon_id INT REFERENCES Polygon(polygon_id),
    lng FLOAT,
    lat FLOAT
);


CREATE TABLE IF NOT EXISTS constraint_reference (
    id UUID PRIMARY KEY, -- Foreign Key, linking to the constraint_id in the ConstraintTable. This field establishes the direct link between the reference and the detailed constraint record.
    manager VARCHAR(255), -- identifier for managing entity
    uss_availability VARCHAR(50) CHECK (uss_availability IN ('', '', '')),-- Enum, state of the USS availability.
    version_number INT, -- Integer, version of the constraint.
    ovn UUID, -- String, opaque version number.
    time_start TIMESTAMPTZ NOT NULL, --TODO check that this is the right format RFC3339-formatted time/date strings, defining the start time. 
    time_end TIMESTAMP WITH TIME ZONE, -- RFC3339-formatted time/date strings, defining the end time.
    uss_base_url TEXT -- String, base URL of the USS.
);


-- Create Geozone Table
CREATE TABLE geozone (
    id UUID PRIMARY KEY,
    identifier VARCHAR(255),
    country VARCHAR(255),
    name VARCHAR(255),
    type VARCHAR(50),
    restriction VARCHAR(255),
    region INT,
    other_reason_info TEXT,
    regulation_exemption VARCHAR(50),
    u_space_class VARCHAR(255),
    message TEXT,
    additional_properties JSONB
);


-- Create Details Table
CREATE TABLE constraint_details (
    id UUID PRIMARY KEY,
    type VARCHAR(255),
    geozone_id UUID,
    FOREIGN KEY (geozone_id) REFERENCES geozone (id)
);


-- Constraints table
CREATE TABLE IF NOT EXISTS constraints_table (
    id UUID PRIMARY KEY,
    reference_id UUID,
    details_id UUID,
    volumes  JSONB, --Volume4D[], -- Array of Volume4D objects, defining the spatial and temporal extents of the constraint.
    type VARCHAR(255), -- String, type of airspace feature.
    FOREIGN KEY (reference_id) REFERENCES constraint_reference (id)
);


-- Create Zone Authority Table
CREATE TABLE zone_authority (
    id UUID PRIMARY KEY,
    geozone_id UUID,
    name VARCHAR(255),
    service VARCHAR(255),
    contact_name VARCHAR(255),
    site_url VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    purpose VARCHAR(50),
    interval_before VARCHAR(255),
    FOREIGN KEY (geozone_id) REFERENCES geozone (id)
);

-- Create Restriction Conditions Table
CREATE TABLE restriction_conditions (
    id UUID PRIMARY KEY,
    geozone_id UUID,
    condition TEXT,
    FOREIGN KEY (geozone_id) REFERENCES geozone (id)
);

-- Create Reason Table
CREATE TABLE reason (
    id UUID PRIMARY KEY,
    geozone_id UUID,
    reason VARCHAR(255),
    FOREIGN KEY (geozone_id) REFERENCES geozone (id)
);

-- from Airspacelink operation
CREATE TABLE pilot_routes (
    uas_id UUID PRIMARY KEY,
    pilot_name VARCHAR(255),
    pilot_phone VARCHAR(20),
    time_start TIMESTAMP WITH TIME ZONE,
    time_end TIMESTAMP WITH TIME ZONE,
    route GEOMETRY(LineString, 4326)
);

-- InterUSS emergency event structure
CREATE TABLE emergency_events (
    event_id VARCHAR PRIMARY KEY,
    timestamp TIMESTAMP,
    uas_id VARCHAR,
    operator_id VARCHAR,
    emergency_type VARCHAR,
    severity_level VARCHAR,
    location GEOGRAPHY(Point, 4326),
    altitude INTEGER,
    affected_area TEXT,
    potential_risk TEXT,
    recommended_actions TEXT,
    communication_details TEXT,
    status VARCHAR,
    update_timestamp TIMESTAMP
);

CREATE TABLE basic_flight_plans (
    flight_plan_id VARCHAR PRIMARY KEY,
    uas_id VARCHAR,
    operator_id VARCHAR,
    plan_intent TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    flight_path GEOGRAPHY(LineString, 4326),
    cruising_altitude INTEGER,
    cruising_speed INTEGER,
    communication_info TEXT,
    usage_state VARCHAR,
    uas_state VARCHAR,
    flight_area GEOGRAPHY(Polygon, 4326),
    execution_style VARCHAR,
    extent GEOGRAPHY(Polygon, 4326),
    success BOOLEAN,
    flight_plan_status VARCHAR,
    planning_activity_result VARCHAR,
    advisory_inclusion VARCHAR
);

ALTER TABLE basic_flight_plans
ADD CONSTRAINT usage_state CHECK (usage_state IN ('Planned', 'InUse', 'Closed')),
ADD CONSTRAINT uas_state CHECK (uas_state IN ('Nominal', 'OffNominal', 'Contingent', 'NotSpecified')),
ADD CONSTRAINT flight_plan_status CHECK (flight_plan_status IN ('NotPlanned', 'Planned', 'OkToFly', 'OffNominal', 'Closed')),
ADD CONSTRAINT planning_activity_result CHECK (planning_activity_result IN ('Completed', 'Rejected', 'Failed', 'NotSupported')),
ADD CONSTRAINT advisory_inclusion CHECK (advisory_inclusion IN ('Unknown', 'AtLeastOneAdvisoryOrCondition', 'NoAdvisoriesOrConditions'));

CREATE TABLE basic_flight_plans_audit (
    audit_id SERIAL PRIMARY KEY,
    operation_type VARCHAR(6) NOT NULL,
    operation_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    operated_by VARCHAR,
    original_flight_plan_id VARCHAR,
    uas_id VARCHAR,
    operator_id VARCHAR,
    plan_intent TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    flight_path GEOGRAPHY(LineString, 4326),
    cruising_altitude INTEGER,
    cruising_speed INTEGER,
    communication_info TEXT,
    usage_state VARCHAR,
    uas_state VARCHAR,
    flight_area GEOGRAPHY(Polygon, 4326),
    execution_style VARCHAR,
    extent GEOGRAPHY(Polygon, 4326),
    success BOOLEAN,
    flight_plan_status VARCHAR,
    planning_result VARCHAR
);

CREATE OR REPLACE FUNCTION log_flight_plan_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO basic_flight_plans_audit (
            operation_type, operated_by, original_flight_plan_id,
            uas_id, operator_id, plan_intent, start_time, end_time,
            flight_path, cruising_altitude, cruising_speed, communication_info,
            usage_state, uas_state, flight_area, execution_style,
            extent, success, flight_plan_status, planning_result
        ) VALUES (
            TG_OP, current_user, OLD.flight_plan_id,
            OLD.uas_id, OLD.operator_id, OLD.plan_intent, OLD.start_time, OLD.end_time,
            OLD.flight_path, OLD.cruising_altitude, OLD.cruising_speed, OLD.communication_info,
            OLD.usage_state, OLD.uas_state, OLD.flight_area, OLD.execution_style,
            OLD.extent, OLD.success, OLD.flight_plan_status, OLD.planning_result
        );
        RETURN OLD;
    ELSE
        INSERT INTO basic_flight_plans_audit (
            operation_type, operated_by, original_flight_plan_id,
            uas_id, operator_id, plan_intent, start_time, end_time,
            flight_path, cruising_altitude, cruising_speed, communication_info,
            usage_state, uas_state, flight_area, execution_style,
            extent, success, flight_plan_status, planning_result
        ) VALUES (
            TG_OP, current_user, NEW.flight_plan_id,
            NEW.uas_id, NEW.operator_id, NEW.plan_intent, NEW.start_time, NEW.end_time,
            NEW.flight_path, NEW.cruising_altitude, NEW.cruising_speed, NEW.communication_info,
            NEW.usage_state, NEW.uas_state, NEW.flight_area, NEW.execution_style,
            NEW.extent, NEW.success, NEW.flight_plan_status, NEW.planning_result
        );
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER flight_plan_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON basic_flight_plans
FOR EACH ROW EXECUTE FUNCTION log_flight_plan_changes();

*/
