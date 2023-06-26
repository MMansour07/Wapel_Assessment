using EMS.Core.Dtos.Role;
using System.Collections.Generic;

namespace EMS.Core.Dtos.UserInRole
{
    public class UserInRoleDto
    {
        public string UserId { get; set; }
        public string Username { get; set; }
        public string RoleId { get; set; }
        public string Rolename { get; set; }
    }

    public class UserInRolesDto
    {
        public string UserId { get; set; }
        public string Username { get; set; }
        public List<RoleDto> Roles { get; set; } 
            = new List<RoleDto>();
    }
}