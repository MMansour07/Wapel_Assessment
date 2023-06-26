using AutoMapper;
using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.Owin;
using Microsoft.Owin.Security;
using EMS.Core.Dtos.User;
using EMS.Core.Helper;
using EMS.Service.Interfaces;
using System;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;

namespace EMS.Webclient.Controllers
{
    public class AccountController : BaseController
    {
        private readonly IAuthService _authService;
        private IMapper _autoMapper;

        private IAuthenticationManager AuthenticationManager
        {
            get
            {
                return HttpContext.GetOwinContext().Authentication;
            }
        }
        public AccountController(IAuthService authService, IMapper autoMapper)
        {
            _authService = authService;
            _autoMapper = autoMapper;
        }

        [HttpGet]
        public ActionResult Register()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> Register(RegisterUserDto model)
        {
            if (ModelState.IsValid)
            {
                var result = await _authService.RegisterUserAsync(model);

                if (result.Success)
                {
                    if(result.Data.Succeeded)
                    return RedirectToAction("Land", "User");

                    AddErrors(result.Data);
                }
                else
                    return RedirectToAction("Acknowledge", new { message = result.Message });
                // handle failure
                // navigate to acknowledge page
            }
            return View(model);
        }

        [HttpGet]
        public ActionResult Login(string returnUrl)
        {
            ViewBag.ReturnUrl = returnUrl;
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> Login(SigninUserDto model, string returnUrl)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }
            var response = await _authService.PasswordSignInAsync(model);
            if (response.Success)
            {
                switch (response.Data)
                {
                    case SignInStatus.Success:
                        if (_authService.UserInRole(model.Email, ERole.SuperAdmin).Data)
                            return RedirectToAction("Land", "User");
                        else
                            return RedirectToAction("Land", "User");
                    case SignInStatus.Failure:
                    default:
                        ModelState.AddModelError("", "Invalid login attempt.");
                        return View(model);
                }
            }
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });
            // handle failure
            // navigate to acknowledge page
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult LogOff()
        {
            AuthenticationManager.SignOut(DefaultAuthenticationTypes.ApplicationCookie);
            return RedirectToAction("Details", "User");
        }
        private void AddErrors(IdentityResult result)
        {
            foreach (var error in result.Errors)
            {
                ModelState.AddModelError("", error);
            }
        }

        private ActionResult RedirectToLocal(string returnUrl)
        {
            if (Url.IsLocalUrl(returnUrl))
            {
                return Redirect(returnUrl);
            }
            return RedirectToAction("Index", "Home");
        }
    }
}