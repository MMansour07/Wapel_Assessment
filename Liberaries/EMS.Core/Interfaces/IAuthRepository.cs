using EMS.Core.Model;
using Microsoft.AspNet.Identity;
using System.Linq;
using System.Threading.Tasks;
using EMS.Core.Dtos.UserInfo;
using System.Linq.Expressions;
using System;
using System.Collections.Generic;
using Microsoft.AspNet.Identity.EntityFramework;
using EMS.Core.Dtos.User;

namespace EMS.Core.Interfaces
{
    public interface IAuthRepository
    {
        #region UsersInRoles

        Task<IdentityResult> RemoveUserFromRolesAsync(string userId);
        Task<IdentityResult> AddUserToRoleAsync(string userId, string rolename);
        Task<IdentityResult> AddUserToRolesAsync(string userId, string[] rolename);
        Task<IdentityResult> RemoveUserFromRoleAsync(string userId, string rolename);

        Task<List<UserSelectListDto>> GetUsersAsSelectList();
        #endregion

        #region Users

        IQueryable<User> Filter(Expression<Func<User, bool>> filter = null, Sort srt = null, Query qry = null,
            Expression<Func<User, bool>> searchfilter = null, string includeProperties = "", bool anotherLevel = false);
        Task<User> FindUserAsync(string id);
        Task<UserInfoDto> FindUserinfoByIdAsync(string id);
        Task<int> UpdateUserActivityAsync(string email);
        Task<IdentityResult> RegisterUserAsync(User user, string password);
        System.Threading.Tasks.Task UpdateAsync(User user);
        Task<IdentityResult> DeleteUserAsync(User user);
        bool UserInRole(string UserId, string RoleId);
        Task<IdentityResult> UpdateUserAsync(User user);

        #endregion

        #region Roles
        Task<List<IdentityRole>> GetRoles();
        #endregion
    }
}
