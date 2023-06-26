using EMS.Core.Dtos.Department;
using EMS.Core.Dtos.Evaluation;
using EMS.Core.Dtos.Rating;
using EMS.Core.Dtos.Role;
using EMS.Core.Dtos.Task;
using EMS.Core.Helper;
using System;
using System.Collections.Generic;
using System.Linq;

namespace EMS.Core.Dtos.User
{
    public class UserDto
    {
        public string Id { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string FullName { get { return FirstName + " " + LastName; } }
        public string CompanyName { get; set; }
        public string Phone { get; set; }
        public string Email { get; set; }
        public string UserName { get; set; }
        public bool IsAdmin
        {
            get
            {
                return this.Roles != null ? Roles.Any(x => x.RoleId == ERole.HR) : false;
            }
        }
        public DateTime? LastActive { get; set; }
        public DepartmentDto Department { get; set; }
        public List<RatingDto> Rating { get; set; }
        public List<TaskDto> Tasks { get; set; }
        public List<GetRoleDto> Roles { get; set; }
        public int RatingCount 
        { 
            get
            {
                return  this.Rating != null ? this.Rating.Count : 0;
            }
        }

        public int TasksCount
        {
            get
            {
                return this.Tasks != null ? this.Tasks.Count : 0;
            }
        }
    }
}