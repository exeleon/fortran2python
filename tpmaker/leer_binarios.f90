MODULE read_binary
       real,  allocatable, dimension (:,:,:) :: p,t
       real,  allocatable, dimension (:,:,:) :: q,wx

CONTAINS

!SUBROUTINE principal(ser,inisam,finsam)
SUBROUTINE readbin(binaryFiles)
      use dimensiones
      use consderper
      use consdernper
      use consderper_f
      use consdernper_f
      use consrs
      use consrs_f
      use funciones 
      use derivvel
      use derivtools
      use velocidades
      use jacobtools
      use mallagrid

!       integer i_sample,n_serie

!       integer ser,inisam,finsam
        !character(100), dimension (:) :: binaryFiles
	character(100) binaryFiles
	integer numFiles

       integer n1,n2,n3
       integer i,j,k,l
!      character(2) serie
!      character(3) sample
      character(100) outputfield
      character(100) inputfield
      real :: rq,r,macref,mac,pref,spl

      CALL INI ()
      CALL MEMORIA ()
      CALL INIDERIV ()

      allocate(t(nx,ny,nz))
      allocate(p(nx,ny,nz))
      allocate(q(nx,ny,nz))
      allocate(wx(nx,ny,nz))

      open(11,file='tpmaker/jet.grid',form='unformatted')
      read(11)nd
      read(11)n1,n2,n3
      read(11)x
      read(11)y
      read(11)z
      close(11)

!	numFiles=size(binaryFiles)
	numFiles=1

!       n_serie=ser
!       i_sample=inisam
!       DO l=inisam,finsam
!         WRITE(sample,'(i3.3)')i_sample
!         WRITE(serie,'(i2.2)')n_serie
	DO l=1,numFiles
	 outputfield=binaryFiles
!        outputfield='field_'//serie//'.'//sample
!        inputfield='prueba.dat'
         OPEN(11,file=outputfield,form='unformatted')
!        OPEN(61,FILE=inputfield,FORM='formatted')
         READ(11)nd
         READ(11)n1,n2,n3
         READ(11)u
         READ(11)v
         READ(11)w
         READ(11)t
         READ(11)p
!         i_sample=i_sample+1

         CALL deriv_VEL()

         DO i=1,nx
       	   DO j=1,ny
       	     DO k=1,nz
               sum=dvel(i,j,k,4)**2+dvel(i,j,k,7)**2+dvel(i,j,k,2)**2+  &
               dvel(i,j,k,8)**2+dvel(i,j,k,3)**2+dvel(i,j,k,6)**2
               sumx=2*(dvel(i,j,k,4)*dvel(i,j,k,2)+dvel(i,j,k,7)*dvel(i,j,k,3)+ &
               dvel(i,j,k,8)*dvel(i,j,k,6))
               Rnorm=0.5*(sum-sumx)
               Snorm=dvel(i,j,k,1)**2+dvel(i,j,k,5)**2+dvel(i,j,k,9)**2+  &
               0.5*(sum+sumx)
               q(i,j,k)=0.5*(Rnorm-Snorm)
               wx(i,j,k)=dvel(i,j,k,8)-dvel(i,j,k,6)
       	     ENDDO
       	   ENDDO
         ENDDO

!         nx=120

 !       write(61,*)'VARIABLES = "X", "Y", "Z", "U", "V", "W", "P", "T"'
 !       write(61,*)'ZONE I=',NX,' J=',NY,' K=',NZ,' DATAPACKING=POINT'
!        DO k=1,nz
!        DO j=1,ny
!        DO i=1,nx
!         r=p(i,j,k)/t(i,j,k)
!         rq=q(i,j,k)
!         if(r.lt.1.)r=1.
!         if(r.gt.2.5)r=2.5
!         if(rq.lt.0.)rq=0.
!         if(rq.gt.25.)rq=25.
!original criterio q         Write(61,100)x(i,j,k),y(i,j,k),z(i,j,k),rq
!         Write(61,100)x(i,j,k),y(i,j,k),z(i,j,k),u(i,j,k),v(i,j,k),w(i,j,k),p(i,j,k),t(i,j,k)
!        enddo
!        enddo
!        enddo

! 100   FORMAT(f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6)
!        CLOSE(11)
!       CLOSE(61)
       ENDDO
!hasta aqui solo imprime una variable
!stop
  


!       OPEN(61,FILE='jet_q.dat',FORM='formatted')

!       nx=120
!       nz=89
!       ny=89

!     write(61,*)'VARIABLES = "X", "Y", "Z", "Q", "P", "SPL", "M", "U", "V", "W"'
!        write(61,*)'ZONE I=',NX,' J=',NY,' K=',NZ,' DATAPACKING=POINT'
!        DO k=11,99
!        DO j=11,99
!        DO i=1,120

!         usqr=sqrt(u(i,j,k)**2.+v(i,j,k)**2.+w(i,j,k)**2.)
!         macref=1.15
!         pref=101.3
        ! mac=macref*(usqr/sqrt(t(i,j,k)))
!         mac=macref*(u(i,j,k)/sqrt(t(i,j,k)))
!         spl=20.*log10(sqrt(p(i,j,k)*pref*1000)/(20E-6))
          
!         Write(61,100)x(i,j,k),y(i,j,k),z(i,j,k),q(i,j,k),p(i,j,k)*pref,    &
!               spl,mac,u(i,j,k),v(i,j,k),w(i,j,k)
!        enddo
!        enddo
!        enddo

!       CLOSE(61)

!       do i=1,nx
!         usqr=sqrt(u(i,55,55)**2.+v(i,55,55)**2.+w(i,55,55)**2.)
!         macref=1.19
!         mac=macref*(usqr/sqrt(1.4*t(i,55,55)))
!        write(6,*)i,mac
!       enddo
!stop
!hasta aqui solo imprime las variables instantaneas 

!        ny=1

!        OPEN(61,FILE='jetc_q.dat',FORM='formatted')
!        write(61,*)'VARIABLES = "X", "Z", "W", "U", "P", "Ma", "R"'
!        write(61,*)'ZONE I=',NX,' J=',NY,' K=',NZ,' DATAPACKING=POINT'
!        DO k=1,nz
!        DO i=1,nx
!         Write(61,200)x(i,55,k),z(i,55,k),w(i,55,k), &
!			      u(i,55,k),p(i,55,k)       &
!          ,u(i,55,k)/sqrt(1.4*t(i,55,k)*(1./(1.4*1.5*1.5))), &
!                      p(i,55,k)/t(i,55,k)
!        enddo
!        enddo
! 200   FORMAT(f12.6,f12.6,f12.6,f12.6,f12.6,f12.6,f12.6)
!       CLOSE(61)
 !      do k=1,nz
!        write(6,*)k,u(1,55,k)
!       enddo

!        OPEN(62,FILE='jetc_bin.dat',FORM='unformatted')
!        write(62)x
!        write(62)y
!        write(62)z
!        write(62)u
!        write(62)v
!        write(62)w
!        write(62)p
!        write(62)wx
!       CLOSE(62)
       return
      END SUBROUTINE readbin


      SUBROUTINE ini()

      use dimensiones
      use consfiltro
      use deltas
      nx=120
      ny=109
      nz=109
      cfilt=0.49
      deltax=float(nx-1)
      deltay=float(ny-1)
      deltaz=float(nz-1)

      end subroutine ini

END MODULE
