using EMS.Service.Interfaces;
using System.Threading.Tasks;
using System.Web.Mvc;
using Microsoft.AspNet.Identity;
using EMS.Core.Dtos.User;
using Microsoft.Owin.Security;
using System.Web;
using EMS.Core.Dtos.General;
using EMS.Core.Helper;
using System.Linq;

namespace EMS.Webclient.Controllers
{
    [Authorize(Roles = ERole.SuperAdmin + "," + ERole.HR)]
    public class UserController : BaseController
    {
        private readonly IAuthService _authService;
        private readonly IDepartmentService _departmentService;
        private IAuthenticationManager AuthenticationManager
        {
            get
            {
                return HttpContext.GetOwinContext().Authentication;
            }
        }
        public UserController(IAuthService authService, IDepartmentService departmentService)
        {
            _authService = authService;
            _departmentService = departmentService;
        }

        [HttpGet]
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<ActionResult> Userlst(RequestModel<string> req)
        {
            var response = await _authService.GetUsers(req);
            if (response.Success)
                return Json(response.Data, JsonRequestBehavior.AllowGet);
            else
                return Json(response.Data, JsonRequestBehavior.AllowGet);
            // handle failure
            // navigate to acknowledge page
        }

        [OverrideAuthorization]
        [Authorize(Roles = ERole.SuperAdmin + "," + ERole.HR + "," + ERole.Employee + "," + ERole.Manager)]
        [HttpGet]
        public async Task<ActionResult> Details(string id, bool isgeneral = false)
        {
            var response = await _authService.GetUserInfoAsync(isgeneral ? id : User.Identity.GetUserId());
            if (response.Success)
                return View(response.Data);
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });
            // handle failure
            // navigate to acknowledge page
        }

        [HttpGet]
        public async Task<ActionResult> New()
        {
            var rolesResponse = await _authService.GetRoles();

            if (rolesResponse.Success)
            {
                ViewBag.Roles = rolesResponse.Data;

                var DepartmnetResponse = await _departmentService.GetDeparments();

                if (DepartmnetResponse.Success)
                {
                    ViewBag.Departments = DepartmnetResponse.Data;

                    var usersResponse = await _authService.GetUsersAsSelectList();

                    ViewBag.Users = usersResponse.Data;

                    if (usersResponse.Success)
                    {
                        return View();
                    }
                    return RedirectToAction("Acknowledge", new { message = usersResponse.Message });
                }
                else
                    return RedirectToAction("Acknowledge", new { message = DepartmnetResponse.Message });
            }
            else
                return RedirectToAction("Acknowledge", new { message = rolesResponse.Message });
            // handle failure
            // navigate to acknowledge page
        }

        [HttpGet]
        public async Task<ActionResult> Edit(string id)
        {
            var response = await _authService.FindUserAsync(id?? User.Identity.GetUserId());

            if (response.Success)
            {
                var rolesResponse = await _authService.GetRoles();

                if (rolesResponse.Success)
                {
                    ViewBag.Roles = rolesResponse.Data;

                    var DepartmnetResponse = await _departmentService.GetDeparments();

                    if (DepartmnetResponse.Success)
                    {
                        ViewBag.Departments = DepartmnetResponse.Data;

                        var usersResponse = await _authService.GetUsersAsSelectList();

                        ViewBag.Users = usersResponse.Data;

                        if (usersResponse.Success)
                        {
                            return View(response.Data);
                        }
                        return RedirectToAction("Acknowledge", new { message = usersResponse.Message });
                    }
                    else
                        return RedirectToAction("Acknowledge", new { message = DepartmnetResponse.Message });
                }
                return RedirectToAction("Acknowledge", new { message = response.Message });
            }
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });
            // handle failure
            // navigate to acknowledge page
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> Edit(UserEditDto user)
        {
            if (ModelState.IsValid)
            {
                var response = await _authService.UpdateUserAsync(user);
                if (response.Success)
                    return RedirectToAction("Index");
                else
                    return RedirectToAction("Acknowledge", new { message = response.Message });
                // handle failure
                // navigate to acknowledge page

            }
            return View(user);
        }



        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> New(NewUserDto user)
        {
            if (ModelState.IsValid)
            {
                var response = await _authService.CreateNewUser(user);
                if (response.Success)
                    return RedirectToAction("Index");
                else
                    return RedirectToAction("Acknowledge", new { message = response.Message });
                // handle failure
                // navigate to acknowledge page

            }

            var rolesResponse = await _authService.GetRoles();

            if (rolesResponse.Success)
            {
                ViewBag.Roles = rolesResponse.Data;

                var DepartmnetResponse = await _departmentService.GetDeparments();

                if (DepartmnetResponse.Success)
                {
                    ViewBag.Departments = DepartmnetResponse.Data;

                    var usersResponse = await _authService.GetUsersAsSelectList();

                    ViewBag.Users = usersResponse.Data;

                    if (usersResponse.Success)
                    {
                        return View();
                    }
                    return RedirectToAction("Acknowledge", new { message = usersResponse.Message });
                }
                else
                    return RedirectToAction("Acknowledge", new { message = DepartmnetResponse.Message });
            }
            else
                return RedirectToAction("Acknowledge", new { message = rolesResponse.Message });
        }

        [HttpGet]
        public async Task<ActionResult> Delete(string id)
        {
            var response = await _authService.FindUserAsync(id?? User.Identity.GetUserId());
            if (response.Success)
                return View(response.Data);
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });
            // handle failure
            // navigate to acknowledge page
        }

        [HttpGet, ActionName("DeleteUser")]
        public async Task<ActionResult> DeleteConfirmed(string id)
        {
            // not soft delete
            var response = await _authService.DeleteUserAsync(id);
            if (response.Success)
            {
                if(response.Data.Succeeded)
                {
                    //AuthenticationManager.SignOut(DefaultAuthenticationTypes.ApplicationCookie);
                    return Json(response, JsonRequestBehavior.AllowGet);
                }
                return View();
            }
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });
            // handle failure
            // navigate to acknowledge page
        }

        [OverrideAuthorization]
        //[Authorize(Roles = ERole.Employee + "," + ERole.HR)]
        [HttpGet]
        public async Task<ActionResult> Land()
        {
            var response = await _authService.GetUserInfoAsync(User.Identity.GetUserId());
            if (response.Success)
                return View(response.Data);
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });
            // handle failure
            // navigate to acknowledge page
        }

        //must be secured against users and only for superadmin for now depenent on show/hide
        [HttpGet]
        public async Task<ActionResult> AddUserToRole(string userId)
        {
            if(!string.IsNullOrEmpty(userId))
            {
                var response = await _authService.AddUserToRoleAsync(userId);
                if (response.Success)
                    return Json(response, JsonRequestBehavior.AllowGet);
            }
            return Json(false, JsonRequestBehavior.AllowGet); // to be handled
        }

        //should be and send data in body
        [HttpGet]
        public async Task<ActionResult> RemoveUserFromRole(string userId)
        {
            if (!string.IsNullOrEmpty(userId))
            {
                var response = await _authService.RemoveUserFromRoleAsync(userId);
                if (response.Success)
                    return Json(response, JsonRequestBehavior.AllowGet);
            }
            return Json(false, JsonRequestBehavior.AllowGet); // to be handled
        }
    }
}