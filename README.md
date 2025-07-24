
# Event_Api

A modern REST API built with FastAPI for managing events with automatic notification simulation for upcoming events.

## Features

- Create, list, and retrieve events with full validation
- Automatic notifications for events starting within 5 minutes
- Clean separation of concerns (models, services, controllers)
- Timezone-aware notification system (Europe/Brussels)
- Automatic API documentation with Swagger UI
- Background worker for continuous event monitoring
- Duplicate notification prevention

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation & Running

1. Clone the repository
```bash
git clone https://github.com/mous11747/Event_Api.git
cd Event_Api
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

**Automatic Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI

### Alternative: Using Docker

```bash
# Build the image
docker build -t event-api .

# Run the container
docker run -p 8000:8000 event-api
```

## API Endpoints

### Create Event
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly team sync",
    "datetime": "2025-07-21T10:30:00"
  }'
```

### List All Events
```bash
curl http://localhost:8000/events
```
Returns events and any triggered notifications.

### Get Specific Event
```bash
curl http://localhost:8000/events/{event-id}
```

### Root Health Check
```bash
curl http://localhost:8000/
```

## Usage Examples

```bash
# Create an event
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Review", 
    "description": "Quarterly project review meeting",
    "datetime": "2025-07-21T14:00:00"
  }'

# List all events
curl http://localhost:8000/events

# Get specific event
curl http://localhost:8000/events/{event-id}

# View interactive docs
open http://localhost:8000/docs
```

## How Notifications Work

The application uses a sophisticated notification system:

### Background Worker
- Runs continuously every 60 seconds
- Checks all events for upcoming start times
- Timezone-aware using Europe/Brussels (CEST)

### Smart Notification Logic
- Triggers for events starting within 5 minutes
- Prevents duplicate notifications with tracking
- Returns notifications in API responses
- Logs detailed timing information to console

### Example Output
```
🕐 Checking for upcoming events...
🔍 Checking notifications at Day 2025-07-21 Time 14:27:30 (Europe/Brussels)
📅 Event 'Team Meeting' is scheduled at Day 2025-07-21 Time 14:30:00 (Europe/Brussels)
  ⏱️ Starts in 150.00 seconds
[Console] 🔔 Event 'Team Meeting' is about to start!
```

## DateTime Format

Events accept ISO format datetime strings:
- `2025-07-21T14:30:00` (recommended)
- `2025-07-21T14:30:00Z` (UTC)
- `2025-07-21T14:30:00+02:00` (with timezone)

All times are converted to Europe/Brussels timezone for notification calculations.

## Architecture

```
app/
├── main.py              # FastAPI app & background tasks
├── models/
│   └── event.py         # Pydantic Event model
├── controllers/
│   └── event_controller.py  # API route handlers  
└── services/
    ├── event_service.py     # Business logic
    └── notification_service.py  # Notification system
```

**Design Patterns:**
- **Repository Pattern**: EventService for data operations
- **Service Layer**: NotificationService for business logic  
- **Controller Layer**: Clean API handlers
- **Model Layer**: Pydantic for validation and serialization

## Testing

Test the API using the interactive Swagger UI at `http://localhost:8000/docs` or manually:

### Manual Testing Steps
1. **Create events**: Add a few test events
2. **Test notifications**: Create an event 2-3 minutes in the future
3. **Watch console**: Monitor background worker output
4. **Validate API**: Check GET endpoints return notifications
5. **Test edge cases**: Try invalid datetime formats, missing fields

### Testing Notifications
```bash
# Create event starting soon (replace with actual future time)
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Notification Test",
    "description": "Should notify soon",
    "datetime": "2025-07-21T15:35:00"
  }'

# Check for notifications in response
curl http://localhost:8000/events
```

## Development Features

### Automatic API Documentation
- **Swagger UI**: `http://localhost:8000/docs` - Interactive testing
- **ReDoc**: `http://localhost:8000/redoc` - Clean documentation
- **OpenAPI Schema**: `http://localhost:8000/openapi.json` - Machine-readable spec

### Hot Reloading
Development server automatically reloads on code changes:
```bash
uvicorn main:app --reload
```

### Type Safety
- Full type hints throughout codebase
- Pydantic models for request/response validation
- IDE support with autocompletion and error detection

---

## If I had more time, I would...

### Code Quality & Testing
- **Comprehensive test suite**: Unit tests with pytest and async test client
- **Integration tests**: End-to-end API testing with test database
- **Code coverage**: Ensure 90%+ test coverage with pytest-cov
- **Linting & formatting**: Black, isort, flake8, mypy for code quality
- **Pre-commit hooks**: Automated code quality checks

### Architecture & Scalability  
- **Database integration**: Replace in-memory storage with PostgreSQL + SQLAlchemy
- **Database migrations**: Alembic for schema versioning
- **Dependency injection**: FastAPI's dependency system for better testability
- **Configuration management**: Pydantic Settings for environment-based config
- **Async database operations**: Async SQLAlchemy for better performance

### Production Readiness
- **Authentication & authorization**: JWT tokens with FastAPI Security
- **Rate limiting**: slowapi for request throttling
- **Input validation**: Custom validators for business rules (e.g., no past events)
- **Error handling**: Custom exception handlers and structured error responses  
- **Logging**: Structured logging with correlation IDs
- **Monitoring**: Prometheus metrics and health checks
- **Security headers**: CORS, CSP, and security middleware

### Background Processing
- **Message queue**: Celery + Redis for reliable background jobs
- **Scheduled tasks**: APScheduler for cron-like event processing
- **Event streaming**: Kafka for real-time event processing
- **Notification channels**: Email, SMS, webhooks with retry logic
- **Dead letter queues**: Handle failed notification attempts

### Features & Functionality
- **Event management**: UPDATE/DELETE operations with soft deletes
- **Event categories**: Tagging and categorization system
- **Recurring events**: Support for daily/weekly/monthly patterns
- **Event search**: Full-text search with filtering and pagination
- **User management**: Multi-tenant support with user isolation
- **Event reminders**: Multiple notification times (1 hour, 1 day before)
- **Time zones**: Per-user timezone preferences
- **Event attachments**: File upload support

### API Enhancements
- **API versioning**: URL-based versioning for backward compatibility  
- **Response pagination**: Cursor-based pagination for large datasets
- **Field filtering**: Allow clients to specify which fields to return
- **Batch operations**: Bulk create/update/delete endpoints
- **WebSocket support**: Real-time event updates
- **GraphQL endpoint**: Alternative query interface
- **API rate limiting**: Per-user quotas and throttling

### DevOps & Deployment
- **CI/CD pipeline**: GitHub Actions with automated testing and deployment
- **Container orchestration**: Kubernetes with Helm charts
- **Infrastructure as code**: Terraform for AWS/GCP provisioning
- **Secret management**: HashiCorp Vault or cloud secret managers
- **Blue-green deployments**: Zero-downtime deployments
- **Monitoring stack**: Grafana, Prometheus, Jaeger for observability
- **Log aggregation**: ELK stack or cloud logging solutions

---

## If this had to serve 10,000 users a day, what would break?

### Immediate Bottlenecks

**1. In-Memory Storage Crisis**
- **Current**: All events stored in Python list, lost on restart
- **Problem**: Memory usage grows unbounded, no persistence, no concurrent access safety
- **Impact**: Data loss, memory leaks, crashes under load

**2. Notification System Inefficiency**  
- **Current**: Checks ALL events on every GET request + background worker
- **Problem**: O(n) complexity per request, duplicate work, resource waste
- **Impact**: API response times degrade linearly with event count

**3. Synchronous Operations**
- **Current**: Some operations block the event loop
- **Problem**: Can't handle 10,000 concurrent requests efficiently
- **Impact**: Request timeouts, poor user experience

### Performance Degradation Points

**4. No Database Indexing**
- **Current**: Linear search through event list
- **Problem**: Event lookups become O(n), no query optimization
- **Impact**: API becomes unusable with 100,000+ events

**5. Memory Consumption**
- **Current**: All events loaded in memory always
- **Problem**: RAM usage scales directly with data size
- **Impact**: Server crashes when memory exhausted

**6. No Caching Layer**
- **Current**: Every request hits data store
- **Problem**: Repeated work for identical queries
- **Impact**: Unnecessary CPU and I/O overhead

**7. Single Point of Failure**
- **Current**: Single server instance
- **Problem**: Any server issue affects all users
- **Impact**: 100% downtime during outages

### Scalability Solutions

**Database Layer**
- **PostgreSQL** with proper indexing on datetime and ID fields
- **Connection pooling** (asyncpg + SQLAlchemy async)
- **Read replicas** for query distribution
- **Database partitioning** by date ranges

**Application Architecture** 
- **Horizontal scaling**: Multiple FastAPI instances behind load balancer
- **Async operations**: Full async/await throughout the stack
- **Connection pooling**: Efficient database connection management
- **Background jobs**: Celery workers for notification processing

**Caching Strategy**
- **Redis** for frequently accessed events and user sessions
- **Application-level caching** with TTL for event lists
- **CDN** for static content and cacheable API responses
- **Query result caching** with invalidation strategies

**Infrastructure Requirements**
- **Load balancer** (nginx/HAProxy) for traffic distribution
- **Auto-scaling** based on CPU/memory metrics
- **Database clustering** with primary/replica setup
- **Message queue** (Redis/RabbitMQ) for background processing

**Monitoring & Performance**
- **APM tools** (New Relic, DataDog) for performance tracking
- **Database query monitoring** to identify slow queries
- **Real-time alerting** for performance degradation
- **Load testing** with tools like k6 or Locust

### Expected Performance Profile

**With Optimizations:**
- **API Response Time**: <100ms for 95% of requests
- **Throughput**: 1000+ requests/second per instance
- **Database**: Sub-millisecond queries with proper indexing
- **Background Processing**: Handle notifications for 100,000+ events
- **Uptime**: 99.9% with proper monitoring and failover

**Resource Requirements:**
- **Application Servers**: 3-5 instances (2 CPU, 4GB RAM each)
- **Database**: PostgreSQL cluster (4 CPU, 16GB RAM primary)
- **Cache**: Redis cluster (2 CPU, 8GB RAM)
- **Load Balancer**: nginx (1 CPU, 2GB RAM)

<<<<<<< HEAD
The current architecture is perfect for development and small-scale usage, but would need significant architectural changes to handle production traffic reliably.
=======
The current architecture is perfect for development and small-scale usage, but would need significant architectural changes to handle production traffic reliably.
>>>>>>> origin/main
