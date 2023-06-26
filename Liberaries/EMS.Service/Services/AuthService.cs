using EMS.Core.Dtos.User;
using EMS.Core.Dtos.UserInfo;
using EMS.Service.Interfaces;
using System.Linq;
using System.Threading.Tasks;
using EMS.Core.Interfaces;
using EMS.Core.Model;
using Microsoft.AspNet.Identity;
using AutoMapper;
using Microsoft.AspNet.Identity.Owin;
using EMS.Data.Identity;
using EMS.Core.Dtos.General;
using System;
using EMS.Core.Helper;
using EMS.Core.Dtos.Role;
using System.Collections.Generic;
using Microsoft.AspNet.Identity.EntityFramework;

namespace EMS.Service
{
    public class AuthService : IAuthService
    {
        private readonly IAuthRepository _identityRepository;
        private IMapper _autoMapper;
        private ApplicationSignInManager _signInManager;
        private readonly IUnitOfWork _unitOfWork;
        public AuthService(IAuthRepository identityRepository, IMapper autoMapper, ApplicationSignInManager signInManager, IUnitOfWork unitOfWork)
        {
            _identityRepository = identityRepository;
            _autoMapper = autoMapper;
            _signInManager = signInManager;
            _unitOfWork = unitOfWork;
        }

        #region Users
        public async Task<ResponseModel<TableModel<UserDto>>> GetUsers(RequestModel<string> obj)
        {
            try
            {
                var users = _identityRepository.Filter(i => i.Roles.Any(r => r.RoleId != ERole.SuperAdmin.ToString()) , obj.sort, obj.query,
                    i => i.UserName.ToLower().Contains(obj.query.generalSearch));

                return new ResponseModel<TableModel<UserDto>>()
                {
                    Success = true,
                    Data = _autoMapper.Map<PagedList<User>, TableModel<UserDto>>(await PagedList<User>.Create(users, obj.pagination.page, obj.pagination.perpage, users.Count()))
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<TableModel<UserDto>>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<List<UserSelectListDto>>> GetUsersAsSelectList()
        {
            try
            {
                var users = await _identityRepository.GetUsersAsSelectList();

                return new ResponseModel<List<UserSelectListDto>>()
                {
                    Success = true,
                    Data = users
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<List<UserSelectListDto>> { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<UserEditDto>> FindUserAsync(string id)
        {
            try
            {
                return new ResponseModel<UserEditDto>() { Data = _autoMapper.Map<User, UserEditDto>(await _identityRepository.FindUserAsync(id)) ?? null, Success = true };
            }
            catch (Exception ex)
            {
                return new ResponseModel<UserEditDto>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<IdentityResult>> RegisterUserAsync(RegisterUserDto userModel)
        {
            try
            {
                var user = _autoMapper.Map<RegisterUserDto, User>(userModel);

                var response = await _identityRepository.RegisterUserAsync(user, userModel.Password);

                if (response.Succeeded)
                {
                    var result  = await _identityRepository.AddUserToRoleAsync(user.Id, ERole.Employee.ToString());

                    if(result.Succeeded)
                    await _signInManager.SignInAsync(user, isPersistent: false, rememberBrowser: false);

                    await _identityRepository.UpdateUserActivityAsync(userModel.Email);

                    return new ResponseModel<IdentityResult>() { Data = response, Success = true};
                }
                else
                    return new ResponseModel<IdentityResult>() { Data = response, Success = true };
            }
            catch (Exception ex)
            {
                //logs + roll back if possible
                return new ResponseModel<IdentityResult>() { Ex = ex, Message = ex.Message, Success = false };
            }

        }

        public async Task<ResponseModel<IdentityResult>> CreateNewUser(NewUserDto userModel)
        {
            try
            {
                var user = _autoMapper.Map<NewUserDto, User>(userModel);

                var response = await _identityRepository.RegisterUserAsync(user, userModel.Password);

                if (response.Succeeded)
                    return new ResponseModel<IdentityResult>() { Data = response, Success = true };
                else
                    return new ResponseModel<IdentityResult>() { Data = response, Success = true };
            }
            catch (Exception ex)
            {
                //logs + roll back if possible
                return new ResponseModel<IdentityResult>() { Ex = ex, Message = ex.Message, Success = false };
            }

        }

        public async Task<ResponseModel<IdentityResult>> AddUserToRoleAsync(string UserId)
        {
            try
            {
                return new ResponseModel<IdentityResult>() { Data = await _identityRepository.AddUserToRoleAsync(UserId, ERole.HR), Success = true };
            }
            catch (Exception ex)
            {
                //logs + roll back if possible
                return new ResponseModel<IdentityResult>() { Ex = ex, Message = ex.Message, Success = false };
            }

        }

        public async Task<ResponseModel<IdentityResult>> RemoveUserFromRoleAsync(string UserId)
        {
            try
            {
                return new ResponseModel<IdentityResult>() { Data = await _identityRepository.RemoveUserFromRoleAsync(UserId, ERole.HR), Success = true };
            }
            catch (Exception ex)
            {
                //logs + roll back if possible
                return new ResponseModel<IdentityResult>() { Ex = ex, Message = ex.Message, Success = false };
            }

        }

        public async Task<ResponseModel<SignInStatus>> PasswordSignInAsync(SigninUserDto userModel)
        {
            try
            {
                var result = await _signInManager.PasswordSignInAsync(userModel.Email, userModel.Password,
                    userModel.RememberMe, shouldLockout: false);

                // in case of success or failure of signing as trial
                await _identityRepository.UpdateUserActivityAsync(userModel.Email);

                return new ResponseModel<SignInStatus>()
                {
                    Data = await _signInManager.PasswordSignInAsync(userModel.Email, userModel.Password, userModel.RememberMe, shouldLockout: false),
                    Success = true
                };
            }
            catch (Exception ex)
            {
                //logs
                return new ResponseModel<SignInStatus>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
        public ResponseModel<bool> UserInRole(string UserName, string RoleId)
        {
            try
            {
                return new ResponseModel<bool>()
                {
                    Data = _identityRepository.UserInRole(UserName, RoleId),
                    Success = true
                };
            }
            catch (Exception ex)
            {
                //logs
                return new ResponseModel<bool>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<object>> UpdateUserAsync(UserEditDto userModel)
        {
            try
            {
                var Deleteresult = await _unitOfWork.authRepository.RemoveUserFromRolesAsync(userModel.Id);

                if (Deleteresult.Succeeded)
                {
                    var addResult = await _unitOfWork.authRepository.AddUserToRolesAsync(userModel.Id, userModel.SelectedRoles.ToArray());

                    if (addResult.Succeeded)
                    {
                        await _unitOfWork.authRepository.UpdateAsync(_autoMapper.Map<UserEditDto, User>(userModel));

                        int status = await _unitOfWork.SaveChanges();

                        if(status == 0)
                        return new ResponseModel<object>() { Data = null, Success = true };
                    }
                }

                return new ResponseModel<object>() { Data = null, Success = false };
            }
            catch (Exception ex)
            {
                //logs
                return new ResponseModel<object>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<IdentityResult>> DeleteUserAsync(string userId)
        {
            try
            {
                var user = await _identityRepository.FindUserAsync(userId);
                if (user != null)
                {
                    return new ResponseModel<IdentityResult>() { Data = await _identityRepository.DeleteUserAsync(user), Success = true };
                }
                return new ResponseModel<IdentityResult>() { Data = IdentityResult.Failed("User is not available"), Success = true };
            }
            catch (Exception ex)
            {
                //logs
                return new ResponseModel<IdentityResult>() { Ex = ex, Message = ex.Message, Success = false };
            }
           
        }

        #endregion

        #region UsersInfos
        public async Task<ResponseModel<UserInfoDto>> GetUserInfoAsync(string userId)
        {
            try
            {
                return new ResponseModel<UserInfoDto>() { Data = await _identityRepository.FindUserinfoByIdAsync(userId), Success = true};
            }
            catch (Exception ex)
            {
                //logs
                return new ResponseModel<UserInfoDto>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
        #endregion


        #region
        public async Task<ResponseModel<List<RoleDto>>> GetRoles()
        {
            try
            {
                var roles = await _identityRepository.GetRoles();

                return new ResponseModel<List<RoleDto>>()
                {
                    Success = true,
                    Data = _autoMapper.Map<List<IdentityRole>, List<RoleDto>>(roles)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<List<RoleDto>>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
        #endregion
    }
}
