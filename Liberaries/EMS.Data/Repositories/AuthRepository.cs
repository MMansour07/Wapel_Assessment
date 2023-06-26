using EMS.Core.Interfaces;
using EMS.Core.Model;
using EMS.Data.Identity;
using Microsoft.AspNet.Identity;
using System;
using System.Data.Entity;
using System.Linq;
using System.Threading.Tasks;
using EMS.Core.Dtos.UserInfo;
using System.Linq.Expressions;
using EMS.Core.Helper;
using System.Collections;
using System.Collections.Generic;
using Microsoft.AspNet.Identity.EntityFramework;
using EMS.Core.Dtos.User;

namespace EMS.Data.Repositories
{
    public class AuthRepository : IAuthRepository, IDisposable
    {
        private DataContext _context;
        private ApplicationUserManager _userManager;
        
        public AuthRepository(DataContext context, ApplicationUserManager userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        #region UsersInRoles
        public async Task<IdentityResult> AddUserToRoleAsync(string userId, string rolename)
        {
            return await _userManager.AddToRoleAsync(userId, rolename);
        }

        public async Task<IdentityResult> AddUserToRolesAsync(string userId, string[] rolenames)
        {
            return await _userManager.AddToRolesAsync(userId, rolenames);
        }
        public async Task<IdentityResult> RemoveUserFromRoleAsync(string userId, string rolename)
        {
            return await _userManager.RemoveFromRoleAsync(userId, rolename);
        }
        public async Task<IdentityResult> RemoveUserFromRolesAsync(string userId)
        {
            return await _userManager.RemoveFromRolesAsync(userId, _userManager.GetRoles(userId).ToArray());
        }
        
        #endregion

        #region Users
        public async Task<User> FindUserAsync(string id)
        {
            return await _userManager.FindByIdAsync(id);
        }

        public async Task<IdentityResult> UpdateUserAsync(User user)
        {
            try
            {
                return await _userManager.UpdateAsync(user);
            }
            catch (Exception ex)
            {

                throw;
            }
        }

        public async Task<UserInfoDto> FindUserinfoByIdAsync(string id)
        {
            return await _context
                .Users
                .Select(u => new UserInfoDto()
                {
                    Id = u.Id,
                    CompanyName = u.CompanyName,
                    Email = u.Email,
                    FirstName = u.FirstName,
                    LastName = u.LastName,
                    Phone = u.Phone,
                    MediaCount = u.Ratings.Count()
                }).FirstOrDefaultAsync(x => x.Id == id);
        }

        public async Task<IdentityResult> RegisterUserAsync(User user, string password)
        {
            user.Roles.ToList().ForEach(x => x.UserId = user.Id);
            return await _userManager.CreateAsync(user, password);
        }

        public async Task<int> UpdateUserActivityAsync(string email)
        {
            var user = _context.Users.SingleOrDefault(r => r.Email == email);
            if (user != null)
            {
                user.LastActive = DateTime.Now;

                _context.Entry(user).State = EntityState.Modified;
                return await _context.SaveChangesAsync();
            }
            return 0;
        }

        public async System.Threading.Tasks.Task UpdateAsync(User user)
        {
            await _context.SingleUpdateAsync(user);
        }

        public bool UserInRole(string UserId, string RoleId)
        {
           return  _context.Users.Where(u => u.Id == UserId).Any(i => i.Roles.Any(r => r.RoleId == RoleId));
        }

        public IQueryable<User> Filter(Expression<Func<User, bool>> filter = null, Sort srt = null, 
            Query qry = null, Expression<Func<User, bool>> searchfilter = null, string includeProperties = "", bool anotherLevel = false)
        {
            IQueryable<User> query = _context.Set<User>();

            if (filter != null)
            {
                if (!string.IsNullOrEmpty(qry?.generalSearch))
                {
                    var parameter = Expression.Parameter(typeof(User));

                    var leftVisitor = new ReplaceExpressionVisitor(filter.Parameters[0], parameter);
                    var left = leftVisitor.Visit(filter.Body);

                    var rightVisitor = new ReplaceExpressionVisitor(searchfilter.Parameters[0], parameter);
                    var right = rightVisitor.Visit(searchfilter.Body);

                    query = query.Where(Expression.Lambda<Func<User, bool>>(Expression.AndAlso(left, right), parameter));
                }
                else
                    query = query.Where(filter);
            }
            if (!string.IsNullOrEmpty(includeProperties))
            {
                foreach (var includeProperty in includeProperties.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
                {
                    query = query.Include(includeProperty);
                }
            }
            if (!string.IsNullOrEmpty(srt?.field))
            {
                var param = Expression.Parameter(typeof(User), string.Empty);
                var property = Expression.PropertyOrField(param, srt.field);
                var sort = Expression.Lambda(property, param);

                var call = Expression.Call(
                    typeof(Queryable),
                    (!anotherLevel ? "OrderBy" : "ThenBy") + ("desc" == srt.sort ? "Descending" : string.Empty),
                    new[] { typeof(User), property.Type },
                    query.Expression,
                    Expression.Quote(sort));

                return query.Provider.CreateQuery<User>(call);
            }

            return query.AsNoTracking();
        }

        public async Task<List<UserSelectListDto>> GetUsersAsSelectList()
        {
            return await _context.Users.Select(x => new UserSelectListDto() { Id = x.Id, FirstName = x.FirstName, LastName = x.LastName}).AsNoTracking().ToListAsync();
        }

        public async Task<IdentityResult> DeleteUserAsync(User user)
        {
            return await _userManager.DeleteAsync(user);
        }
        #endregion

        #region Roles
        public async Task<List<IdentityRole>> GetRoles()
        {
            return await _context.Roles.Where(i => i.Id != ERole.SuperAdmin).AsNoTracking().ToListAsync();
        }
        #endregion

        private bool disposed = false;

        protected virtual void Dispose(bool disposing)
        {
            if (!disposed)
            {
                if (disposing)
                {
                    _context.Dispose();
                    _userManager.Dispose();
                }
            }
            disposed = true;
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }
    }
}