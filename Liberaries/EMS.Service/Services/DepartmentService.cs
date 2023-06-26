using AutoMapper;
using EMS.Core.Dtos.General;
using EMS.Core.Interfaces;
using EMS.Core.Model;
using EMS.Service.Interfaces;
using System.Threading.Tasks;
using System;
using System.Collections.Generic;
using EMS.Core.Dtos.Department;
using System.Linq;
using System.Data.Entity;

namespace EMS.Service.Services
{
    public class DepartmentService : IDepartmentService
    {
        private readonly IRepository<Department> _iDepartmentRepository;
        private IMapper _autoMapper;
        public DepartmentService(IMapper autoMapper, IRepository<Department> iDepartmentRepository)
        {
            _autoMapper = autoMapper;
            _iDepartmentRepository = iDepartmentRepository;
        }

        public async Task<ResponseModel<List<DepartmentDto>>> GetDeparments()
        {
            try
            {
                var Departments = await _iDepartmentRepository.GetAll();
                
                return new ResponseModel<List<DepartmentDto>>()
                {
                    Success = true,
                    Data = _autoMapper.Map<List<Department>, List<DepartmentDto>>(Departments)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<List<DepartmentDto>>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
    }
}
