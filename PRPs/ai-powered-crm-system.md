name: "AI-Powered CRM System with Multi-Model Intelligence"
description: |

## Purpose
Comprehensive PRP for building a production-ready AI-powered CRM system using Node.js backend, HTML5/CSS/ES6 frontend, MongoDB database, and OpenRouter API for multi-model AI integration. This system enables automated task generation, timeline creation, and pipeline management through intelligent AI assistance.

## Core Principles
1. **Context is King**: 60+ pages of research documentation provide complete implementation guidance
2. **Validation Loops**: Executable tests and lints for iterative refinement  
3. **Information Dense**: Real examples and patterns from official documentation
4. **Progressive Success**: Start with core CRM, then add AI features
5. **Global rules**: Follow all rules in CLAUDE.md

---

## Goal
Build a complete AI-powered CRM system where users can:
- Create tasks and have AI automatically generate detailed subtasks with dependencies
- Get AI-generated timelines with milestones and estimated completion dates
- Manage customers through automated pipeline stages with AI-driven insights
- Access the system via a public marketing frontend and authenticated dashboard backend
- Experience real-time AI processing with live updates and progress indicators

**End State**: Production-ready CRM with seamless AI integration that enhances productivity without complexity.

## Why
- **Business Value**: Automates routine CRM tasks, reduces manual planning overhead, improves project accuracy
- **User Impact**: Sales and marketing teams get intelligent assistance for task planning and timeline estimation
- **Integration Needs**: Bridges marketing website with full-featured CRM dashboard behind authentication
- **Problems Solved**: Manual task breakdown, inaccurate time estimation, pipeline management inefficiency
- **Market Opportunity**: AI-enhanced productivity tools are in high demand across sales and marketing teams

## What
A full-stack CRM application with intelligent AI assistance:

### User-Visible Behavior
1. **Marketing Frontend**: Public website with demo, pricing, contact forms
2. **Authentication Layer**: Secure login/register system with role-based access
3. **CRM Dashboard**: Complete task management, customer tracking, pipeline visualization
4. **AI Task Generation**: Create a task → AI generates subtasks, dependencies, and timelines automatically
5. **Real-time Updates**: Live progress indicators during AI processing with WebSocket connections
6. **Pipeline Automation**: Customers move through sales/marketing funnels with AI-triggered actions

### Technical Requirements
- **Backend**: Node.js + Express.js + MongoDB with real-time Socket.IO integration
- **Frontend**: HTML5/CSS/ES6 component-based architecture (NO React)
- **AI Integration**: OpenRouter API with GPT-4o-mini and Gemini 2.5 Pro models
- **Database**: MongoDB with optimized schemas for CRM workflows
- **Authentication**: JWT-based with marketing frontend + dashboard backend separation
- **Performance**: Real-time AI processing with progress feedback <2 seconds response time

### Success Criteria
- [ ] Marketing frontend loads and captures leads effectively
- [ ] Authentication system supports role-based access (admin, sales, marketing)
- [ ] Task creation triggers AI subtask generation within 10 seconds
- [ ] AI-generated timelines include dependencies and realistic date estimates
- [ ] Pipeline automation moves customers through stages automatically
- [ ] Real-time updates show AI processing progress with <400ms UI feedback
- [ ] System handles 100+ concurrent users with <2 second response times
- [ ] All AI features gracefully degrade when API is unavailable
- [ ] Mobile-responsive design works on all device sizes
- [ ] Complete test coverage with passing validation loops

## All Needed Context

### Documentation & References
```yaml
# MUST READ - AI Integration Research
- docfile: research/openrouter/RESEARCH_SUMMARY.md
  why: Complete OpenRouter API integration patterns, model specifications, pricing
  critical: GPT-4o-mini and Gemini 2.5 Pro model setup, cost optimization strategies
  
- docfile: research/openrouter/page1_quickstart.md
  why: OpenRouter API authentication and basic integration patterns
  
- docfile: research/openrouter/page22_gpt_4o_mini.md
  why: Specific model configuration for fast/cheap AI operations
  
- docfile: research/openrouter/page23_gemini_2_5_pro.md
  why: Configuration for slow/expensive high-quality AI operations

# MUST READ - Backend Architecture Research  
- docfile: research/nodejs-mongodb/architectural_summary.md
  why: Complete MongoDB data modeling for CRM, authentication patterns, API design
  critical: CRM collections schema, indexing strategies, real-time integration
  
- docfile: research/nodejs-mongodb/page2_express_routing.md
  why: Express.js routing patterns for CRM API endpoints
  
- docfile: research/nodejs-mongodb/page11_jwt_authentication.md
  why: JWT implementation for marketing frontend + dashboard backend separation
  
- docfile: research/nodejs-mongodb/page10_socketio_realtime.md
  why: WebSocket integration for real-time AI processing updates

# MUST READ - Frontend Architecture Research
- docfile: research/frontend-ai-ux/frontend-ai-ux-recommendations.md
  why: AI UX patterns, component architecture for HTML5/CSS/ES6 (adapted from React patterns)
  critical: AI progress indicators, user feedback loops, responsive design system
  
- docfile: research/frontend-ai-ux/page2-ai-ux-getting-started.md
  why: AI integration UX principles and best practices
  
- docfile: research/frontend-ai-ux/page4-tailwind-css-framework.md
  why: Utility-first CSS framework for consistent design system

# MUST READ - AI Agent Architecture (Translation Reference)
- docfile: research/pydantic-ai/RESEARCH_SUMMARY.md
  why: AI agent patterns to translate from Python to Node.js implementation
  critical: Multi-agent workflows, tool integration, structured outputs, conversation management
  
- docfile: research/pydantic-ai/page3-agents.md
  why: Agent architecture patterns for JavaScript implementation
  
- docfile: research/pydantic-ai/page5-examples.md
  why: Real-world AI agent examples and implementation patterns

# External Documentation URLs
- url: https://openrouter.ai/docs/quickstart
  why: Live OpenRouter API documentation and authentication setup
  section: Authentication, Model Selection, Function Calling
  
- url: https://expressjs.com/en/guide/routing.html
  why: Express.js routing for CRM API endpoints
  
- url: https://mongoosejs.com/docs/guide.html
  why: MongoDB object modeling for CRM data structures
  
- url: https://socket.io/docs/v4/
  why: Real-time WebSocket integration for AI processing updates
```

### Current Codebase Tree
```bash
.
├── CLAUDE.md                    # Project instructions and coding guidelines
├── initial.md                   # Feature requirements and API specifications
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md         # PRP template structure
│   └── EXAMPLE_multi_agent_prp.md # Multi-agent system example
├── research/                    # Comprehensive research documentation
│   ├── pydantic-ai/            # AI agent architecture research (20 pages)
│   ├── openrouter/             # Multi-model API research (23 pages)
│   ├── nodejs-mongodb/         # Backend architecture research (15 pages)
│   └── frontend-ai-ux/         # Frontend UX research (6 pages)
└── tests/                      # Test directory (empty)
```

### Desired Codebase Tree
```bash
.
├── backend/
│   ├── package.json            # Node.js dependencies and scripts
│   ├── server.js               # Express.js server setup and middleware
│   ├── config/
│   │   ├── database.js         # MongoDB connection and configuration
│   │   ├── auth.js             # JWT authentication configuration
│   │   └── openrouter.js       # OpenRouter API client setup
│   ├── models/
│   │   ├── User.js             # User authentication and profile schema
│   │   ├── Customer.js         # Customer/lead data schema
│   │   ├── Task.js             # Task and subtask schema with AI metadata
│   │   └── Pipeline.js         # Sales/marketing pipeline schema
│   ├── routes/
│   │   ├── auth.js             # Authentication endpoints (login, register, refresh)
│   │   ├── customers.js        # Customer CRUD operations
│   │   ├── tasks.js            # Task management with AI generation endpoints
│   │   ├── pipelines.js        # Pipeline management and automation
│   │   └── dashboard.js        # Dashboard statistics and analytics
│   ├── services/
│   │   ├── aiService.js        # OpenRouter AI integration service
│   │   ├── taskGenerator.js    # AI-powered task and timeline generation
│   │   ├── pipelineAutomation.js # Pipeline stage automation logic
│   │   └── realTimeService.js  # Socket.IO real-time update handling
│   ├── middleware/
│   │   ├── auth.js             # JWT token validation middleware
│   │   ├── validation.js       # Request data validation
│   │   └── rateLimiting.js     # API rate limiting and security
│   └── utils/
│       ├── logger.js           # Logging utility
│       ├── errorHandler.js     # Centralized error handling
│       └── helpers.js          # Common utility functions
├── frontend/
│   ├── index.html              # Marketing landing page
│   ├── dashboard.html          # Main CRM dashboard
│   ├── login.html              # Authentication page
│   ├── css/
│   │   ├── tailwind.min.css    # Tailwind CSS framework
│   │   ├── components.css      # Custom component styles
│   │   └── dashboard.css       # Dashboard-specific styles
│   ├── js/
│   │   ├── main.js             # Entry point and app initialization
│   │   ├── auth.js             # Authentication handling
│   │   ├── api.js              # API client and HTTP utilities
│   │   ├── components/
│   │   │   ├── TaskCard.js     # Task display component
│   │   │   ├── AIProgress.js   # AI processing progress indicator
│   │   │   ├── Pipeline.js     # Pipeline visualization component
│   │   │   └── Dashboard.js    # Dashboard layout and widgets
│   │   ├── services/
│   │   │   ├── aiService.js    # Frontend AI service integration
│   │   │   ├── socketService.js # Real-time WebSocket handling
│   │   │   └── stateManager.js # Application state management
│   │   └── utils/
│   │       ├── helpers.js      # Utility functions
│   │       ├── constants.js    # Application constants
│   │       └── validation.js   # Form validation utilities
├── tests/
│   ├── backend/
│   │   ├── auth.test.js        # Authentication endpoint tests
│   │   ├── tasks.test.js       # Task management tests
│   │   ├── aiService.test.js   # AI integration tests
│   │   └── integration.test.js # Full system integration tests
│   └── frontend/
│       ├── components.test.js  # Frontend component tests
│       └── e2e.test.js         # End-to-end user workflow tests
├── docker-compose.yml          # MongoDB and app containerization
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore patterns
├── README.md                   # Setup and deployment documentation
└── package.json                # Root project configuration
```

### Known Gotchas & Library Quirks
```javascript
// CRITICAL: OpenRouter API requires specific headers for proper functionality
// Example: Must include HTTP-Referer and X-Title for API rankings
const openRouterConfig = {
  baseURL: "https://openrouter.ai/api/v1",
  headers: {
    "Authorization": "Bearer " + process.env.OPENROUTER_API_KEY,
    "HTTP-Referer": process.env.SITE_URL, // Required for API rankings
    "X-Title": process.env.SITE_NAME      // Required for API rankings
  }
}

// CRITICAL: MongoDB connection requires proper indexing for CRM performance
// Task queries by assignedTo + status + priority must be indexed
// Customer email must be unique index
// Pipeline stages require compound indexing for automation

// CRITICAL: JWT tokens need both access and refresh token pattern
// Access tokens: 15 minutes expiry for security
// Refresh tokens: 7 days expiry stored in secure HTTP-only cookies

// CRITICAL: Socket.IO requires CORS configuration for frontend integration
// Must configure origins for both development and production environments

// CRITICAL: OpenRouter models have different rate limits
// GPT-4o-mini: 20 req/min on free tier, good for fast operations
// Gemini 2.5 Pro: Higher cost but better quality for complex AI tasks

// CRITICAL: AI task generation must handle timeouts gracefully
// Set 30-second timeout for AI requests with fallback to simpler models
// Implement retry logic with exponential backoff for failed requests

// CRITICAL: Frontend must work without framework dependencies
// Use ES6 modules for component-like architecture
// Implement manual DOM manipulation and event handling
// Use modern JavaScript features (async/await, destructuring, modules)
```

## Implementation Blueprint

### Data Models and Structure

```javascript
// User Schema - Authentication and Profile Management
const UserSchema = {
  _id: ObjectId,
  email: String, // unique index
  password: String, // bcrypt hashed
  role: String, // 'admin', 'sales', 'marketing'
  profile: {
    firstName: String,
    lastName: String,
    department: String,
    avatar: String,
    permissions: [String] // granular permissions
  },
  refreshTokens: [String], // For JWT refresh token rotation
  lastLogin: Date,
  isActive: Boolean,
  createdAt: Date,
  updatedAt: Date
}

// Customer Schema - CRM Core Entity with Lead Tracking
const CustomerSchema = {
  _id: ObjectId,
  contactInfo: {
    email: String, // unique index
    phone: String,
    company: String,
    name: { first: String, last: String },
    website: String
  },
  address: {
    street: String,
    city: String,
    state: String,
    country: String,
    zipCode: String
  },
  status: String, // 'lead', 'prospect', 'customer', 'inactive'
  source: String, // 'website', 'referral', 'cold-call', 'social'
  assignedTo: ObjectId, // ref to Users
  pipelineStage: String,
  pipelineId: ObjectId,
  tags: [String],
  customFields: Map,
  notes: [{
    content: String,
    author: ObjectId,
    createdAt: Date
  }],
  createdAt: Date,
  updatedAt: Date
}

// Task Schema - AI-Enhanced Task Management with Subtasks and Timelines
const TaskSchema = {
  _id: ObjectId,
  title: String,
  description: String,
  status: String, // 'pending', 'in_progress', 'completed', 'cancelled'
  priority: String, // 'low', 'medium', 'high', 'urgent'
  
  // AI-Generated Content and Metadata
  aiGenerated: {
    subtasks: [{
      _id: ObjectId,
      title: String,
      description: String,
      estimatedTime: Number, // minutes
      dependencies: [ObjectId], // other subtask IDs
      status: String,
      assignedTo: ObjectId,
      order: Number
    }],
    timeline: {
      estimatedStartDate: Date,
      estimatedEndDate: Date,
      totalEstimatedTime: Number, // minutes
      milestones: [{
        name: String,
        date: Date,
        completed: Boolean,
        description: String
      }]
    },
    metadata: {
      generatedBy: String, // AI model used (gpt-4o-mini or gemini-2.5-pro)
      confidence: Number, // 0-1 confidence score
      promptUsed: String, // For debugging and improvement
      generatedAt: Date,
      regenerationCount: Number
    }
  },
  
  // Task Relationships and Organization
  customerId: ObjectId, // ref to Customers
  assignedTo: ObjectId, // ref to Users
  parentTask: ObjectId, // for hierarchical tasks
  pipelineStage: String,
  pipelineId: ObjectId,
  
  // Scheduling and Deadlines
  dueDate: Date,
  scheduledFor: Date,
  completedAt: Date,
  
  // Metadata
  createdBy: ObjectId,
  createdAt: Date,
  updatedAt: Date
}

// Pipeline Schema - Sales/Marketing Automation Workflows
const PipelineSchema = {
  _id: ObjectId,
  name: String,
  type: String, // 'sales', 'marketing', 'support', 'onboarding'
  description: String,
  stages: [{
    _id: ObjectId,
    name: String,
    order: Number,
    description: String,
    automations: [{
      trigger: String, // 'entry', 'time_based', 'task_completion', 'manual'
      condition: String, // JavaScript expression for conditional automation
      action: String, // 'create_task', 'send_email', 'assign_user', 'move_stage'
      aiPrompt: String, // For AI-generated task creation
      config: {
        delayMinutes: Number,
        assignToRole: String,
        emailTemplate: String,
        taskTemplate: String
      }
    }],
    exitCriteria: [String] // Conditions for moving to next stage
  }],
  isActive: Boolean,
  createdBy: ObjectId,
  analytics: {
    totalCustomers: Number,
    conversionRates: [{
      fromStage: String,
      toStage: String,
      rate: Number,
      avgTimeInStage: Number
    }]
  },
  createdAt: Date,
  updatedAt: Date
}
```

### List of Tasks to be Completed (Implementation Order)

```yaml
Task 1: Environment Setup and Project Structure
CREATE backend/package.json:
  - EXPRESS framework with Socket.IO for real-time features
  - MONGOOSE for MongoDB object modeling
  - JSONWEBTOKEN for authentication
  - BCRYPTJS for password hashing
  - AXIOS for OpenRouter API integration
  - CORS for frontend-backend communication
  - DOTENV for environment variable management

CREATE frontend file structure:
  - ORGANIZE HTML files for marketing, dashboard, and authentication
  - SETUP Tailwind CSS for utility-first styling
  - CREATE ES6 module structure for component-like architecture

CREATE .env.example:
  - INCLUDE all required environment variables
  - DOCUMENT OpenRouter API key, MongoDB URI, JWT secrets
  - SET proper development and production configurations

Task 2: MongoDB Database Setup and Connection
CREATE config/database.js:
  - ESTABLISH MongoDB connection with Mongoose
  - CONFIGURE connection pooling for production performance
  - IMPLEMENT connection error handling and retry logic
  - CREATE database initialization and seeding scripts

CREATE MongoDB indexes:
  - IMPLEMENT performance indexes for CRM queries
  - UNIQUE index on user emails and customer emails
  - COMPOUND indexes for task queries by assignedTo + status + priority
  - INDEX pipeline stages for automation performance

Task 3: Authentication System Implementation
CREATE models/User.js:
  - IMPLEMENT Mongoose schema with validation
  - INCLUDE password hashing with bcrypt
  - ADD role-based permissions structure
  - CREATE user profile management methods

CREATE routes/auth.js:
  - IMPLEMENT login endpoint with JWT token generation
  - CREATE register endpoint with validation
  - ADD refresh token rotation for security
  - IMPLEMENT logout with token blacklisting

CREATE middleware/auth.js:
  - VALIDATE JWT tokens on protected routes
  - IMPLEMENT role-based access control
  - CREATE user context injection for requests
  - ADD rate limiting for authentication endpoints

Task 4: OpenRouter AI Service Integration
CREATE config/openrouter.js:
  - CONFIGURE OpenRouter API client with proper headers
  - IMPLEMENT multi-model routing (GPT-4o-mini for fast, Gemini 2.5 Pro for quality)
  - ADD retry logic with exponential backoff
  - CREATE usage tracking and cost monitoring

CREATE services/aiService.js:
  - IMPLEMENT chat completion wrapper for task generation
  - CREATE prompt templates for different AI operations
  - ADD response parsing and validation
  - IMPLEMENT error handling with model fallbacks

Task 5: Core Data Models and CRUD Operations
CREATE models/Customer.js, Task.js, Pipeline.js:
  - IMPLEMENT Mongoose schemas with comprehensive validation
  - ADD pre/post middleware for automation triggers
  - CREATE static methods for complex queries
  - IMPLEMENT data aggregation methods for analytics

CREATE routes/customers.js, tasks.js, pipelines.js:
  - IMPLEMENT full CRUD operations with validation
  - ADD filtering, sorting, and pagination
  - CREATE bulk operations for efficiency
  - IMPLEMENT soft delete for data preservation

Task 6: AI-Powered Task Generation Service
CREATE services/taskGenerator.js:
  - IMPLEMENT AI prompt engineering for subtask generation
  - CREATE timeline estimation algorithms using AI
  - ADD dependency detection and ordering logic
  - IMPLEMENT confidence scoring for AI suggestions

CREATE routes/tasks.js AI endpoints:
  - ADD /api/tasks/:id/generate-subtasks endpoint
  - CREATE /api/tasks/:id/generate-timeline endpoint
  - IMPLEMENT /api/tasks/:id/optimize-schedule endpoint
  - ADD progress tracking for long-running AI operations

Task 7: Real-Time WebSocket Integration
CREATE services/realTimeService.js:
  - IMPLEMENT Socket.IO server configuration
  - CREATE room-based user connections
  - ADD AI processing progress broadcasting
  - IMPLEMENT real-time task updates and notifications

INTEGRATE WebSocket with AI services:
  - EMIT progress updates during AI generation
  - BROADCAST task completion notifications
  - CREATE live pipeline movement updates
  - ADD real-time collaboration features

Task 8: Pipeline Automation System
CREATE services/pipelineAutomation.js:
  - IMPLEMENT stage transition logic
  - CREATE automation trigger evaluation
  - ADD AI-powered task creation from pipeline rules
  - IMPLEMENT scheduled automation execution

INTEGRATE with task and customer models:
  - ADD pipeline stage change hooks
  - CREATE automatic task assignment based on rules
  - IMPLEMENT email notifications for stage transitions
  - ADD analytics tracking for pipeline performance

Task 9: Frontend Component Architecture (HTML5/CSS/ES6)
CREATE js/components/ modules:
  - IMPLEMENT TaskCard.js for task display with AI indicators
  - CREATE AIProgress.js for real-time AI processing feedback
  - ADD Pipeline.js for drag-and-drop pipeline visualization
  - IMPLEMENT Dashboard.js for metric displays and quick actions

CREATE js/services/ frontend services:
  - IMPLEMENT apiService.js for backend communication
  - CREATE socketService.js for real-time WebSocket handling
  - ADD stateManager.js for application state without frameworks
  - IMPLEMENT authService.js for JWT token management

Task 10: Marketing Frontend and Dashboard Integration
CREATE index.html marketing page:
  - IMPLEMENT responsive design with Tailwind CSS
  - ADD lead capture forms with validation
  - CREATE demo request and contact functionality
  - IMPLEMENT smooth transitions to dashboard login

CREATE dashboard.html CRM interface:
  - IMPLEMENT modular component loading with ES6 imports
  - ADD real-time updates with Socket.IO integration
  - CREATE responsive grid layout for different screen sizes
  - IMPLEMENT AI feature discovery and onboarding

Task 11: Testing and Quality Assurance
CREATE comprehensive test suite:
  - IMPLEMENT unit tests for all API endpoints
  - ADD integration tests for AI service workflows
  - CREATE end-to-end tests for complete user journeys
  - IMPLEMENT performance tests for concurrent usage

CREATE test data and mocking:
  - IMPLEMENT realistic test data generation
  - ADD AI service mocking for consistent testing
  - CREATE automated testing pipelines
  - IMPLEMENT test coverage reporting

Task 12: Production Deployment and Optimization
CREATE Docker containerization:
  - IMPLEMENT multi-stage Docker builds
  - ADD MongoDB service configuration
  - CREATE production environment configuration
  - IMPLEMENT health checks and monitoring

CREATE performance optimizations:
  - IMPLEMENT API response caching strategies
  - ADD database query optimization
  - CREATE CDN integration for static assets
  - IMPLEMENT monitoring and logging solutions
```

### Per Task Pseudocode

```javascript
// Task 6: AI-Powered Task Generation Service
class TaskGenerator {
  async generateSubtasks(mainTask, customerContext) {
    // PATTERN: Multi-model approach for cost optimization
    const models = [
      { name: "openai/gpt-4o-mini", maxTokens: 1000, cost: "low" },
      { name: "google/gemini-2.5-pro", maxTokens: 2000, cost: "high" }
    ];
    
    // Choose model based on task complexity and priority
    const selectedModel = this.selectModel(mainTask.priority, mainTask.complexity);
    
    const prompt = this.buildTaskPrompt(mainTask, customerContext);
    
    try {
      // CRITICAL: Set 30-second timeout for AI requests
      const response = await this.aiService.chatCompletion({
        model: selectedModel.name,
        messages: [{ role: "user", content: prompt }],
        max_tokens: selectedModel.maxTokens,
        temperature: 0.3, // Lower temperature for more consistent task generation
        response_format: { type: "json_object" } // Structured output
      });
      
      const parsedResponse = JSON.parse(response.choices[0].message.content);
      
      // PATTERN: Validate AI response structure
      const validatedSubtasks = this.validateSubtasks(parsedResponse);
      
      // PATTERN: Calculate dependencies and timeline
      const timeline = await this.generateTimeline(validatedSubtasks, mainTask);
      
      return {
        subtasks: validatedSubtasks,
        timeline: timeline,
        metadata: {
          generatedBy: selectedModel.name,
          confidence: this.calculateConfidence(parsedResponse),
          promptUsed: prompt,
          generatedAt: new Date()
        }
      };
    } catch (error) {
      // GOTCHA: Fallback to simpler model if primary fails
      if (selectedModel.cost === "high") {
        return this.generateSubtasks(mainTask, customerContext, "fallback");
      }
      throw new AIGenerationError("Task generation failed", error);
    }
  }
  
  buildTaskPrompt(mainTask, customerContext) {
    return `
      Generate detailed subtasks for the following CRM task:
      
      Main Task: "${mainTask.title}"
      Description: "${mainTask.description}"
      Priority: ${mainTask.priority}
      
      Customer Context:
      - Company: ${customerContext.company}
      - Industry: ${customerContext.industry}
      - Stage: ${customerContext.pipelineStage}
      
      Requirements:
      1. Break down into 3-8 actionable subtasks
      2. Estimate time for each subtask in minutes
      3. Identify dependencies between subtasks
      4. Provide realistic timeline with milestones
      
      Return JSON format:
      {
        "subtasks": [
          {
            "title": "string",
            "description": "string",
            "estimatedTime": number,
            "dependencies": [subtask_indexes],
            "priority": "low|medium|high"
          }
        ],
        "totalEstimatedTime": number,
        "confidence": number,
        "assumptions": ["list of assumptions made"]
      }
    `;
  }
}

// Task 7: Real-Time WebSocket Integration
class RealTimeService {
  constructor(server) {
    this.io = socketIo(server, {
      cors: {
        origin: process.env.FRONTEND_URL,
        credentials: true
      }
    });
    
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    this.io.on('connection', (socket) => {
      // PATTERN: Authenticate socket connections
      socket.on('authenticate', async (token) => {
        try {
          const user = await this.validateSocketToken(token);
          socket.userId = user._id;
          socket.userRole = user.role;
          
          // Join user-specific room for private notifications
          socket.join(`user:${user._id}`);
          
          // Join role-based rooms for broadcast notifications
          socket.join(`role:${user.role}`);
          
          socket.emit('authenticated', { status: 'success', user: user.profile });
        } catch (error) {
          socket.emit('auth_error', { message: 'Invalid token' });
          socket.disconnect();
        }
      });
      
      // PATTERN: Real-time AI progress updates
      socket.on('subscribe_ai_progress', (taskId) => {
        socket.join(`ai_progress:${taskId}`);
      });
      
      socket.on('disconnect', () => {
        // Cleanup: Leave all rooms
        Object.keys(socket.rooms).forEach(room => {
          socket.leave(room);
        });
      });
    });
  }
  
  // CRITICAL: Broadcast AI generation progress
  async broadcastAIProgress(taskId, progress) {
    this.io.to(`ai_progress:${taskId}`).emit('ai_progress_update', {
      taskId,
      progress: {
        stage: progress.stage, // 'analyzing', 'generating', 'optimizing', 'complete'
        percentage: progress.percentage,
        message: progress.message,
        estimatedTimeRemaining: progress.eta
      }
    });
  }
  
  // CRITICAL: Notify task assignments and updates
  async notifyTaskUpdate(task, updateType) {
    // Notify assigned user
    this.io.to(`user:${task.assignedTo}`).emit('task_update', {
      type: updateType, // 'created', 'updated', 'completed'
      task: task,
      timestamp: new Date()
    });
    
    // Notify team members if task is high priority
    if (task.priority === 'high' || task.priority === 'urgent') {
      this.io.to(`role:admin`).emit('high_priority_task', {
        task: task,
        assignee: task.assignedUser
      });
    }
  }
}

// Task 9: Frontend Component Architecture (ES6 Modules)
class TaskCard {
  constructor(container, task, options = {}) {
    this.container = container;
    this.task = task;
    this.options = options;
    this.element = null;
    
    this.init();
  }
  
  init() {
    this.render();
    this.attachEventListeners();
    
    // PATTERN: Subscribe to real-time updates
    if (this.task._id) {
      socketService.subscribe(`task:${this.task._id}`, this.handleTaskUpdate.bind(this));
    }
  }
  
  render() {
    const html = `
      <div class="task-card bg-white rounded-lg shadow-sm border border-gray-200 p-6 
                  hover:shadow-md transition-shadow duration-200" 
           data-task-id="${this.task._id}">
        
        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-lg font-semibold text-gray-900">${this.task.title}</h3>
          <div class="status-badge ${this.getStatusClass()}">${this.task.status}</div>
        </div>
        
        <!-- Content -->
        <p class="text-gray-600 text-sm mb-4">${this.task.description}</p>
        
        <!-- AI Indicators -->
        ${this.renderAIIndicators()}
        
        <!-- Progress -->
        ${this.renderProgress()}
        
        <!-- Footer -->
        <div class="flex justify-between items-center mt-4 pt-4 border-t border-gray-100">
          <div class="flex items-center space-x-2">
            <img src="${this.task.assignee?.avatar}" 
                 class="w-8 h-8 rounded-full" 
                 alt="${this.task.assignee?.name}">
            <span class="text-sm text-gray-600">${this.task.assignee?.name}</span>
          </div>
          <span class="text-xs text-gray-500">Due: ${this.formatDate(this.task.dueDate)}</span>
        </div>
      </div>
    `;
    
    this.element = this.createElementFromHTML(html);
    this.container.appendChild(this.element);
  }
  
  renderAIIndicators() {
    if (!this.task.aiGenerated) return '';
    
    const confidence = this.task.aiGenerated.metadata?.confidence || 0;
    const confidenceColor = confidence > 0.8 ? 'green' : confidence > 0.6 ? 'yellow' : 'red';
    
    return `
      <div class="ai-indicators bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-blue-700 font-medium text-sm">🤖 AI Generated</span>
          <div class="confidence-badge bg-${confidenceColor}-100 text-${confidenceColor}-700 px-2 py-1 rounded text-xs">
            ${Math.round(confidence * 100)}% confidence
          </div>
        </div>
        
        <div class="ai-stats text-xs text-blue-600">
          <span>${this.task.aiGenerated.subtasks?.length || 0} subtasks</span>
          <span class="mx-2">•</span>
          <span>${this.task.aiGenerated.timeline?.totalEstimatedTime || 0} min estimated</span>
          <span class="mx-2">•</span>
          <span>Generated by ${this.task.aiGenerated.metadata?.generatedBy}</span>
        </div>
      </div>
    `;
  }
  
  // CRITICAL: Handle real-time updates from WebSocket
  handleTaskUpdate(data) {
    if (data.type === 'ai_progress') {
      this.updateAIProgress(data.progress);
    } else if (data.type === 'task_updated') {
      this.task = { ...this.task, ...data.task };
      this.updateDisplay();
    }
  }
  
  updateAIProgress(progress) {
    const progressElement = this.element.querySelector('.ai-progress');
    if (progressElement) {
      progressElement.innerHTML = `
        <div class="flex items-center mb-2">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          <span class="ml-2 text-blue-700 text-sm">${progress.message}</span>
        </div>
        <div class="w-full bg-blue-200 rounded-full h-2">
          <div class="bg-blue-600 h-2 rounded-full transition-all duration-300"
               style="width: ${progress.percentage}%"></div>
        </div>
      `;
    }
  }
}
```

### Integration Points
```yaml
DATABASE:
  - MongoDB connection: "mongodb://localhost:27017/ai_crm"
  - Create indexes for performance:
    - "users.email" (unique)
    - "customers.contactInfo.email" (unique)
    - "tasks.assignedTo, tasks.status, tasks.priority" (compound)
    - "pipelines.stages.order" (ascending)

ENVIRONMENT_VARIABLES:
  - MONGODB_URI: MongoDB connection string
  - JWT_SECRET: Secret for JWT token signing
  - JWT_REFRESH_SECRET: Secret for refresh token signing
  - OPENROUTER_API_KEY: "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"
  - SITE_URL: Frontend URL for OpenRouter headers
  - SITE_NAME: Application name for OpenRouter headers
  - PORT: Server port (default 3000)
  - NODE_ENV: Environment (development/production)

API_ENDPOINTS:
  - Authentication: /api/auth/* (login, register, refresh, logout)
  - Customers: /api/customers/* (CRUD operations)
  - Tasks: /api/tasks/* (CRUD + AI generation endpoints)
  - Pipelines: /api/pipelines/* (automation management)
  - Dashboard: /api/dashboard/* (analytics and stats)
  - Real-time: WebSocket connection on /socket.io

FRONTEND_INTEGRATION:
  - Static files served from /frontend directory
  - API calls using fetch() with JWT authentication
  - WebSocket connection for real-time updates
  - Responsive design using Tailwind CSS utility classes
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
cd backend
npm run lint                    # ESLint for JavaScript code quality
npm run format                  # Prettier for code formatting
npm run test:syntax             # Basic syntax validation

# Expected: No errors. If errors, READ the error message and fix code.
```

### Level 2: Unit Tests
```javascript
// backend/tests/auth.test.js
describe('Authentication System', () => {
  test('should register new user with valid data', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'securePassword123',
      firstName: 'Test',
      lastName: 'User',
      role: 'sales'
    };
    
    const response = await request(app)
      .post('/api/auth/register')
      .send(userData)
      .expect(201);
    
    expect(response.body).toHaveProperty('user');
    expect(response.body).toHaveProperty('token');
    expect(response.body.user.email).toBe(userData.email);
  });
  
  test('should authenticate existing user', async () => {
    const loginData = {
      email: 'test@example.com',
      password: 'securePassword123'
    };
    
    const response = await request(app)
      .post('/api/auth/login')
      .send(loginData)
      .expect(200);
    
    expect(response.body).toHaveProperty('token');
    expect(response.body).toHaveProperty('refreshToken');
  });
});

// backend/tests/aiService.test.js
describe('AI Task Generation', () => {
  test('should generate subtasks for valid task', async () => {
    const taskData = {
      title: 'Launch marketing campaign',
      description: 'Create and execute Q4 marketing campaign',
      priority: 'high'
    };
    
    const customerContext = {
      company: 'TechCorp',
      industry: 'Software',
      pipelineStage: 'qualified'
    };
    
    const result = await taskGenerator.generateSubtasks(taskData, customerContext);
    
    expect(result).toHaveProperty('subtasks');
    expect(result.subtasks).toBeInstanceOf(Array);
    expect(result.subtasks.length).toBeGreaterThan(0);
    expect(result).toHaveProperty('timeline');
    expect(result.metadata.confidence).toBeGreaterThan(0);
  });
  
  test('should handle AI service failures gracefully', async () => {
    // Mock AI service failure
    jest.spyOn(aiService, 'chatCompletion').mockRejectedValue(new Error('API Error'));
    
    const taskData = { title: 'Test task', priority: 'low' };
    const customerContext = { company: 'Test Corp' };
    
    await expect(taskGenerator.generateSubtasks(taskData, customerContext))
      .rejects
      .toThrow('Task generation failed');
  });
});
```

```bash
# Run tests iteratively until passing:
npm test                        # Run all unit tests
npm run test:coverage           # Run tests with coverage report
npm run test:integration        # Run integration tests

# If failing: Read error output, understand root cause, fix code, re-run
# Target: 80%+ test coverage for all critical functions
```

### Level 3: Integration Tests
```bash
# Start MongoDB (ensure it's running)
mongod --dbpath ./data/db

# Start the backend server in test mode
NODE_ENV=test npm start

# Test complete user workflows
echo "Testing user registration and task creation workflow..."
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "integration@test.com",
    "password": "testPassword123",
    "firstName": "Integration",
    "lastName": "Test",
    "role": "sales"
  }'

# Expected: {"user": {...}, "token": "...", "refreshToken": "..."}

echo "Testing AI task generation..."
# Save token from previous response for authentication
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN_FROM_REGISTER>" \
  -d '{
    "title": "Develop client proposal",
    "description": "Create comprehensive proposal for enterprise client",
    "priority": "high",
    "customerId": "placeholder_customer_id"
  }'

# Expected: Task created with AI-generated subtasks and timeline

echo "Testing real-time WebSocket connection..."
# Open WebSocket connection and verify real-time updates
node tests/websocket-test.js

# Expected: Successful connection, authentication, and real-time task updates
```

### Level 4: Frontend Integration Tests
```bash
# Start frontend development server
cd frontend
python -m http.server 8080    # Simple HTTP server for static files

# Open browser and test complete user flows
echo "Test marketing page to dashboard flow..."
# 1. Visit http://localhost:8080
# 2. Fill out contact form
# 3. Navigate to login page
# 4. Register new account
# 5. Access dashboard
# 6. Create new task
# 7. Verify AI subtask generation
# 8. Check real-time updates

# Expected: Smooth user experience with working AI features
```

## Final Validation Checklist
- [ ] All unit tests pass: `npm test`
- [ ] No linting errors: `npm run lint`
- [ ] Integration tests successful with MongoDB connection
- [ ] OpenRouter AI service generates subtasks correctly
- [ ] Real-time WebSocket updates work properly
- [ ] Authentication system supports JWT tokens
- [ ] Frontend loads without framework dependencies
- [ ] Marketing page captures leads effectively
- [ ] Dashboard displays AI-generated content
- [ ] Mobile responsive design works on all devices
- [ ] Error handling graceful for AI service failures
- [ ] Performance targets met: <2 second response times
- [ ] Security measures implemented: rate limiting, input validation
- [ ] Documentation complete: README.md with setup instructions

---

## Anti-Patterns to Avoid
- ❌ Don't use React or other frameworks - stick to HTML5/CSS/ES6
- ❌ Don't hardcode API keys - use environment variables
- ❌ Don't skip AI service error handling - implement fallbacks
- ❌ Don't ignore rate limits for OpenRouter API
- ❌ Don't skip MongoDB indexing - performance will suffer
- ❌ Don't use sync operations in async contexts
- ❌ Don't skip JWT token validation on protected routes
- ❌ Don't ignore WebSocket connection management
- ❌ Don't skip input validation - security vulnerability
- ❌ Don't skip test coverage - breaks in production

## Confidence Score: 9/10

**High confidence due to:**
- Comprehensive research across 60+ documentation pages
- Clear technical specifications with working examples
- Proven architecture patterns from production systems
- Complete validation loops with executable tests
- Specific model configurations and API integrations
- Real-world CRM requirements addressed thoroughly

**Minor uncertainty areas:**
- OpenRouter API rate limits under high load (mitigated with fallback strategies)
- AI generation time optimization (addressed with progress indicators)
- Complex task dependency resolution (handled with validation loops)

This PRP provides sufficient context and implementation guidance for one-pass development success with iterative refinement through the validation loops.