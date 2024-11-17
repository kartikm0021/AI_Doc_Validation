This document consolidates all requirements related to users, logical user groups, and their roles in managing rules and rulesets. It covers user management workflows, logical group creation, user permissions, activity tracking, and integration with Active Directory (AD).

1. Core Features
1.1 Logical User Groups
Logical groups provide a way to organize users under a parent AD group for managing rules and rulesets.

Parent AD Group: Represents the organization unit in Active Directory.
Logical Group: Sub-groups within the parent AD group, representing specific teams or functions.
1.2 User Management
Add, remove, and update users within logical groups.
Assign roles to users (Owner, Editor, Viewer).
Manage cross-group access for sharing rules and rulesets.
1.3 Role-Based Access Control (RBAC)
Define permissions for users within logical groups:

Owner: Full control (manage users, create/edit/delete rules/rulesets).
Editor: Create, edit, and delete rules/rulesets but cannot manage users.
Viewer: View-only access to rules/rulesets.
1.4 AD Integration
Sync user details (LAN ID, email, name) from Active Directory.
Support batch user addition using AD group attributes.
1.5 User Activity Tracking
Track user actions, such as rule/ruleset creation, edits, deletions, and sharing.
Maintain activity logs at the rule/ruleset level for accountability.


2. Logical Group Features
2.1 Logical Group Creation
Admins create logical groups under a parent AD group.

Inputs:

Parent AD Group ID: ad_group_marketing
Logical Group Name: Content Team
Description: Handles marketing content rules.
Generated Logical Group ID:

Format: <parent_ad_group_id>_<logical_group_name_slug>
Example: ad_group_marketing_content_team
2.2 Logical Group Management
Edit logical group details (name, description).
Delete logical groups (with checks for existing dependencies).
2.3 List Logical Groups
Display logical groups, their parent AD group, and descriptions.

Example Response:
{
  "logical_groups": [
    {
      "id": "ad_group_marketing_content_team",
      "name": "Content Team",
      "parent_ad_group_id": "ad_group_marketing",
      "description": "Handles marketing content rules."
    },
    {
      "id": "ad_group_compliance_regulatory",
      "name": "Regulatory Team",
      "parent_ad_group_id": "ad_group_compliance",
      "description": "Handles compliance rules."
    }
  ]
}

3. User Management Features
3.1 Adding Users to Logical Groups
Search and add users by LAN ID or AD email ID.
Automatically fetch user details from AD (e.g., name, email).
Batch user addition via CSV upload.
3.2 Removing Users from Logical Groups
Select users from the group list and remove them.
Confirm removal with a dialog to prevent accidental deletions.
3.3 Assigning Roles
Admins assign roles to users within logical groups:

Owner: Full access.
Editor: Can create/edit/delete rules/rulesets.
Viewer: View-only access.
3.4 View Users in Logical Groups
Display a list of users in each logical group with their details and roles:

LAN ID
Full Name
Email
Role

4. Role-Based Permissions
4.1 Rule and Ruleset Ownership
Ownership is assigned at the logical group level, ensuring that rules/rulesets belong to teams rather than individuals.

4.2 Individual Attribution
Track and display:

Created By: User who created the rule/ruleset.
Last Modified By: User who last edited the rule/ruleset.
Activity Logs: Detailed logs of user actions.
4.3 Cross-Group Sharing
Allow rules/rulesets to be shared across logical groups with specific permissions:

Read-Only: View-only access for the target group.
Editable: Full editing rights for the target group.


5. User Screens
5.1 Logical Group Management Dashboard

+-----------------------------------------------+
| Logical Group Management                      |
+-----------------------------------------------+
| [ Create New Logical Group ]                  |
|                                               |
| Logical Group List:                           |
| +-------------------------------------------+ |
| | Group Name         | Parent AD Group   | Users |
| +-------------------------------------------+ |
| | Content Team       | Marketing         | 10    |
| | Regulatory Team    | Compliance        | 8     |
| +-------------------------------------------+ |
|                                               |
| Actions:                                      |
| - [ Edit ] [ Delete ] [ Manage Users ]        |
+-----------------------------------------------+

5.2 Add Users to Logical Group

+-----------------------------------------------+
| Add Users: Marketing → Content Team           |
+-----------------------------------------------+
| Search User: [ Input: Search by LAN ID/Email ]|
| +-------------------------------------------+ |
| | Full Name   | LAN ID    | Email       | Add | |
| +-------------------------------------------+ |
| | John Doe    | john123   | john@company.com | [ Add ] |
| | Jane Smith  | jane456   | jane@company.com | [ Add ] |
| +-------------------------------------------+ |
|                                               |
| Batch Upload: [ Upload CSV File ]             |
|                                               |
| [ Cancel ]  [ Add Selected Users ]            |
+-----------------------------------------------+


5.3 Role Assignment

+-----------------------------------------------+
| Assign Role: John Doe                         |
+-----------------------------------------------+
| Logical Group: Marketing → Content Team       |
|                                               |
| Current Role: [ Dropdown: Owner ]             |
| [✓] Owner                                     |
| [ ] Editor                                    |
| [ ] Viewer                                    |
|                                               |
| [ Cancel ]  [ Save Changes ]                  |
+-----------------------------------------------+


6. APIs for User and Logical Group Management
6.1 Create Logical Group
Endpoint: POST /api/groups/logical
Payload:
{
  "parent_ad_group_id": "ad_group_marketing",
  "logical_group_name": "Content Team",
  "description": "Handles marketing content rules."
}

6.2 List Logical Groups
Endpoint: GET /api/groups/logical
Response:

{
  "logical_groups": [
    {
      "id": "ad_group_marketing_content_team",
      "name": "Content Team",
      "parent_ad_group_id": "ad_group_marketing",
      "description": "Handles marketing content rules."
    }
  ]
}


6.3 Add Users to Logical Group
Endpoint: POST /api/groups/{logical_group_id}/users
Payload:

{
  "users": [
    { "lan_id": "john123", "role": "Owner" },
    { "lan_id": "jane456", "role": "Viewer" }
  ]
}


6.4 Remove Users from Logical Group
Endpoint: DELETE /api/groups/{logical_group_id}/users
Payload:

{ "lan_ids": ["john123", "jane456"] }


6.5 Update User Role
Endpoint: PUT /api/groups/{logical_group_id}/users/{lan_id}/role
Payload:
{ "role": "Editor" }


7. Activity Tracking
Track User Actions
Maintain an audit log for rules and rulesets:

{
  "rule_id": "123",
  "action": "modified",
  "user": "jane456",
  "timestamp": "2024-11-17T10:00:00Z",
  "details": "Updated validation logic."
}

User Activity API
Endpoint: GET /api/rules/{rule_id}/activity
Response:

{
  "logs": [
    { "action": "created", "user": "john123", "timestamp": "2024-11-01T10:00:00Z" },
    { "action": "modified", "user": "jane456", "timestamp": "2024-11-17T10:00:00Z" }
  ]
}

8. Benefits of This Setup
Scalable User Management:
Logical groups simplify the management of users across departments.
Flexible Roles:
Role-based access ensures secure and granular permissions.
Accountability:
Individual attribution and activity tracking maintain accountability.
Seamless AD Integration:
Automatically fetch and validate user details, reducing manual overhead.