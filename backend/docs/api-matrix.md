# FlawFinder AI - API Matrix Documentation

This document maps the frontend API calls to the corresponding backend endpoints.

## Authentication

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| Login form submission | `/api/v1/auth/login` | POST | User authentication |
| Registration form | `/api/v1/auth/register` | POST | User registration |
| Token refresh | `/api/v1/auth/refresh` | POST | Refresh access token |
| Logout | `/api/v1/auth/logout` | POST | User logout |
| Get current user | `/api/v1/auth/me` | GET | Get user profile |

## Process Flows

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| Upload workflow | `/api/v1/flows` | POST | Create new process flow |
| List workflows | `/api/v1/flows` | GET | Get user's flows |
| Get workflow details | `/api/v1/flows/{id}` | GET | Get specific flow |
| Parse workflow | `/api/v1/flows/{id}/parse` | POST | Parse and analyze flow |
| Get brutality score | `/api/v1/flows/{id}/score` | GET | Calculate brutality score |
| Get role-based fixes | `/api/v1/flows/{id}/fixes?role={role}` | GET | Get fixes by role |

## Reports

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| Generate CEO report | `/api/v1/reports/ceo` | POST | Create CEO report |
| List reports | `/api/v1/reports` | GET | Get user's reports |
| Get report details | `/api/v1/reports/{id}` | GET | Get specific report |
| Download report | `/api/v1/reports/{id}/download` | GET | Download report file |

## AgentOps (ML Pipeline Operations)

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|--------|-------------|
| Register pipeline | `/api/v1/agentops/pipelines` | POST | Register ML pipeline |
| List pipelines | `/api/v1/agentops/pipelines` | GET | Get user's pipelines |
| Get pipeline details | `/api/v1/agentops/pipelines/{id}` | GET | Get specific pipeline |
| Monitor drift | `/api/v1/agentops/pipelines/{id}/monitor` | POST | Capture drift metrics |
| Trigger retraining | `/api/v1/agentops/pipelines/{id}/retrain` | POST | Trigger model retraining |
| Get pipeline status | `/api/v1/agentops/pipelines/{id}/status` | GET | Get pipeline health |

## Request/Response Formats

### Authentication

**Login Request:**
```json
{
  "email": "admin@flawfinder.ai",
  "password": "password123"
}
```

**Login Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Process Flow

**Create Flow Request:**
```json
{
  "name": "HR Approval Process",
  "description": "Employee onboarding approval workflow",
  "raw_input": "The HR approval process starts when a manager submits a new hire request...",
  "organization_id": 1
}
```

**Flow Response:**
```json
{
  "id": 1,
  "name": "HR Approval Process",
  "description": "Employee onboarding approval workflow",
  "version": 1,
  "status": "draft",
  "brutality_score": null,
  "user_id": 1,
  "organization_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Brutality Score

**Score Response:**
```json
{
  "flow_id": 1,
  "score": 73.0,
  "breakdown": {
    "wait_times": 25.0,
    "manual_handoffs": 30.0,
    "rework_loops": 18.0
  },
  "version": "1.0"
}
```

### CEO Report

**Report Request:**
```json
{
  "flow_id": 1,
  "include_departments": true,
  "format": "pdf"
}
```

**Report Response:**
```json
{
  "id": 1,
  "title": "CEO Report - Process Analysis",
  "report_type": "ceo_report",
  "status": "completed",
  "content": {
    "executive_summary": {
      "brutality_score": 73,
      "total_flaws": 42,
      "fixes_implemented": 18
    },
    "key_findings": [...],
    "recommendations": [...]
  },
  "file_url": "/reports/ceo-report.pdf",
  "user_id": 1,
  "process_flow_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": {
    "code": "400",
    "message": "Bad request",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

## Authentication Headers

Protected endpoints require the Authorization header:

```
Authorization: Bearer <access_token>
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (Frontend dev server)
- `http://localhost:3000` (Alternative frontend port)

## Rate Limiting

- 60 requests per minute per user
- Rate limit headers included in responses

## File Upload

File uploads are handled through the `/api/v1/flows` endpoint with multipart/form-data:
- Supported formats: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG, SVG, JSON
- Maximum file size: 10MB

## Environment Variables

The frontend should set these environment variables:

```javascript
// Frontend environment variables
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=FlawFinder AI
```

## Integration Notes

1. **Token Management**: Store JWT tokens in localStorage and refresh before expiration
2. **Error Handling**: Use consistent error response format for all API calls
3. **Loading States**: Implement loading indicators for async operations
4. **File Uploads**: Use FormData for file uploads with progress tracking
5. **Real-time Updates**: Consider WebSocket connections for real-time updates (future enhancement) 