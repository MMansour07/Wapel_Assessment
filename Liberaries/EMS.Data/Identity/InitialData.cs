using EMS.Core.Model;
using Microsoft.AspNet.Identity.EntityFramework;
using System.Collections.Generic;
using System.Linq;
using System;
using System.Security.Cryptography;
using EMS.Core.Helper;

namespace EMS.Data.Identity
{
    public static class InitialData
    {
        // can be transformed to JSON file
        public static List<User> GetAdminUsers()
        {
            var users = new List<User>
            {
                //admin pass: abc123@ -> change later
                new User
                {
                    Id = "e7f18795-000c-4afe-995f-b71ec95fee30",
                    Email = "superadmin@info.com",
                    UserName = "superadmin@info.com",
                    FirstName = "Super",
                    LastName = "Admin",
                    CreatedDate = DateTime.Now,
                    PasswordHash = HashPassword("P@ssw0rd"),
                    SecurityStamp = "3656ca8d-bcf0-4e6d-8d49-81e7da37fd6d"
                }
            };
            return users;
        }

        public static List<IdentityRole> GetRoles()
        {
            return new List<IdentityRole>
            {
                new IdentityRole
                {
                    Id = "SuperAdmin",
                    Name = "SuperAdmin"
                },
                new IdentityRole
                {
                    Id = "HR",
                    Name = "HR"
                },
                new IdentityRole
                {
                    Id = "Employee",
                    Name = "Employee"
                },
                new IdentityRole
                {
                    Id = "Manager",
                    Name = "Manager"
                }
            };
        }

        public static List<Department> GetDepartments()
        {
            return new List<Department>
            {
                new Department
                {
                    Title = "HR"
                },
                new Department
                {
                    Title = "Development"
                },
            };
        }

        public static List<IdentityUserRole> GetUsersInRoles()
        {
            var usersInRoles = new List<IdentityUserRole>();

            var adminUsers = GetAdminUsers();

            var adminRole = GetRoles().SingleOrDefault(r => r.Name == ERole.SuperAdmin);

            if (adminRole != null)
            {
                foreach (var adminUser in adminUsers)
                {
                    usersInRoles.Add(new IdentityUserRole
                    {
                        RoleId = adminRole.Id,
                        UserId = adminUser.Id
                    });
                }
            }
            return usersInRoles;
        }

        public static string HashPassword(string password)
        {
            byte[] salt;
            byte[] buffer2;
            if (password == null)
            {
                throw new ArgumentNullException("password");
            }
            using (Rfc2898DeriveBytes bytes = new Rfc2898DeriveBytes(password, 0x10, 0x3e8))
            {
                salt = bytes.Salt;
                buffer2 = bytes.GetBytes(0x20);
            }
            byte[] dst = new byte[0x31];
            Buffer.BlockCopy(salt, 0, dst, 1, 0x10);
            Buffer.BlockCopy(buffer2, 0, dst, 0x11, 0x20);
            return Convert.ToBase64String(dst);
        }

    }
}